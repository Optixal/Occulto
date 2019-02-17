#!/usr/bin/env python3

import sys
import plyvel
import zstandard as zstd
import replacer
import hasher
import time
import pyshoco
import json
from datetime import datetime
from pathlib import Path

if len(sys.argv) < 2:
    print('Usage: {} dump_directory ...'.format(sys.argv[0]))
    exit(1)

dbLocation = '/home/optixal/Documents/github/Occulto/TestDB/'
db = plyvel.DB(dbLocation, create_if_missing=True)

chunkSize = 131072
chunksPerBatch = 2048
print(f'Using chunkSize: {chunkSize}, chunksPerBatch: {chunksPerBatch}')

totalNewPasswords = 0
totalNewUsernames = 0
totalProcessed = 0
totalDuration = 0

dbMetaLocation = '/home/optixal/Documents/github/Occulto/MetaDB'
dbMeta = plyvel.DB(dbMetaLocation, create_if_missing=True)

for archive in Path(sys.argv[1]).rglob('*.zst'):
# for archive in sys.argv[1:]:
    # archive = Path(archive)

    # Check whether this dump has been added before
    hash = hasher.xxhashsum(archive).encode()
    results = dbMeta.get(hash)
    if results:
        results = json.loads(results)
        if results['completed']:
            print('[*] Skipping {} ({}) as it has already been indexed.'.format(archive, hash.decode()))
            continue

    meta = {
        'count': {
            'new': {
                'passwords': 0,
                'usernames': 0,
            },
            'skipped': {
                'parse_errors': 0,
                'repeated_passwords': 0,
                'empty_passwords': 0,
                'too_long_passwords': 0,
            },
            'total_creds_processed': 0,
            'chunks_read': 0,
            'batches_processed': 0,
        },
        'size': archive.stat().st_size,
        'added_on': datetime.now().timestamp(), #.strftime('%Y-%m-%d %H:%M:%S'),
        'file': str(archive),
        'tag': 'Collection #1',
        'completed': False,
        'chunk_size_used': chunkSize,
        'batch_size_used': chunksPerBatch,
        'duration': 0,
    }
    batch = db.write_batch(transaction=True)
    saved = None
    startTime = time.time()
    buffer = {}

    print('[{}] [{:.2f} MB] Processing ... '.format(archive, meta['size'] / 2 ** 20), end='')

    try:
        with open(archive, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            reader = dctx.stream_reader(f)
            while True:
                chunk = reader.read(chunkSize)
                if not chunk: break
                if saved:
                    chunk = saved + chunk
                    saved = None
                splitted = chunk.split(b'\r\n')
                trail = splitted.pop()
                if trail:
                    saved = trail

                for cred in splitted:
                    meta['count']['total_creds_processed'] += 1
                    try:
                        username, password = cred.split(b':', 1)
                    except ValueError:
                        meta['count']['skipped']['parse_errors'] += 1
                        continue
                    if not password:
                        meta['count']['skipped']['empty_passwords'] += 1
                        continue
                    if len(password) > 512:
                        meta['count']['skipped']['too_long_passwords'] += 1
                        continue

                    username = username.lower() # assumes all usernames/emails are case insensitive
                    username = replacer.compress(username)
                    username = pyshoco.compress(username) # flash compress

                    passwordsInBuffer = buffer.get(username) # returns list of passwords
                    if passwordsInBuffer: # db has already queried this email in this batch and results exists in buffer
                        if password in passwordsInBuffer: # skip if buffer already has password in it, as it is already going to be written
                            meta['count']['skipped']['repeated_passwords'] += 1
                            continue
                        buffer[username].append(password)
                    else:
                        passwordsInDB = db.get(username) # returns single password delimeted with '\x00'
                        if passwordsInDB:
                            passwordsInDB = passwordsInDB.split(b'\x00')
                            if password in passwordsInDB: # skip if password already in DB
                                meta['count']['skipped']['repeated_passwords'] += 1
                                continue
                            passwordsInDB.append(password)
                            buffer[username] = passwordsInDB
                        else:
                            meta['count']['new']['usernames'] += 1
                            buffer[username] = [password]
                    meta['count']['new']['passwords'] += 1

                meta['count']['chunks_read'] += 1
                if meta['count']['chunks_read'] % chunksPerBatch == 0:
                    for username, passwords in buffer.items():
                        batch.put(username, b'\x00'.join(passwords))
                    buffer = {}
                    batch.write()
                    batch.clear()
                    meta['count']['batches_processed'] += 1

            for username, passwords in buffer.items():
                batch.put(username, b'\x00'.join(passwords))
            buffer = {}
            batch.write()
            batch.clear()
            meta['count']['batches_processed'] += 1

    except KeyboardInterrupt:
        break

    else:
        if meta['count']['total_creds_processed'] > 0:
            meta['completed'] = True

    finally:
        totalNewPasswords += meta['count']['new']['passwords']
        totalNewUsernames += meta['count']['new']['usernames']
        totalProcessed += meta['count']['total_creds_processed']
        meta['duration'] = time.time() - startTime
        totalDuration += meta['duration']

        dbMeta.put(hash, json.dumps(meta).encode())
        print('{}. Took {:.2f}s, {:.0f} creds/s, {} creds processed, {} new passwords, {} new usernames/emails.'.format('SUCCESS' if meta['completed'] else 'FAILED', meta['duration'], meta['count']['total_creds_processed'] / meta['duration'] if meta['duration'] > 0 else 0, meta['count']['total_creds_processed'], meta['count']['new']['passwords'], meta['count']['new']['usernames']))

db.close()
dbMeta.close()
print('[+] Done! Total duration {:.2f}s, {:.0f} avg creds/s, {} total creds processed, {} total new passwords, {} total new usernames/emails.'.format(totalDuration, totalProcessed / totalDuration if totalDuration > 0 else 0, totalProcessed, totalNewPasswords, totalNewUsernames))


