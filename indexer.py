#!/usr/bin/env python3

import sys
import plyvel
import zstandard as zstd
import replacer
import time
import pyshoco

if len(sys.argv) < 2:
    print('Usage: {} archive [archive2] ...'.format(sys.argv[0]))
    exit(1)

dbLocation = '/home/optixal/Apps/Occulto/TestDB/'
db = plyvel.DB(dbLocation, create_if_missing=True)
batch = db.write_batch()
decompressor = zstd.ZstdDecompressor()

blockSize = 1024 * 16
batchBlocks = 4096
print(f'Using blockSize: {blockSize}, batchBlocks: {batchBlocks}')

totalSuccess = 0
totalSkipped = 0
totalProcessed = 0
totalDuration = 0

for archive in sys.argv[1:]:

    successCount = 0
    skipCount = 0
    processedCount = 0
    batchCount = 0
    saved = None
    startTime = time.time()
    buffer = {}

    with open(archive, 'rb') as f:
        for chunk in decompressor.read_to_iter(f, read_size=blockSize):
            if saved:
                chunk = saved + chunk
                saved = None
            splitted = chunk.split(b'\r\n')
            trail = splitted.pop()
            if trail:
                saved = trail

            for cred in splitted:
                try:
                    username, password = cred.split(b':', 1)
                except ValueError:
                    # print('[-] Could not parse: {}'.format(cred))
                    skipCount += 1
                    continue
                if not password or len(password) > 512:
                    # print('[-] Skipping, empty or too long: {}'.format(cred))
                    skipCount += 1
                    continue

                username = username.lower() # assumes all usernames/emails are case insensitive
                username = replacer.compress(username)
                username = pyshoco.compress(username) # flash compress

                passwordsInBuffer = buffer.get(username) # returns list of passwords
                if passwordsInBuffer: # db has already queried for this batch block and results exists in buffer
                    if password in passwordsInBuffer: # skip if buffer already has password in it, as it is already going to be written
                        skipCount += 1
                        continue
                    buffer[username].append(password)
                else:
                    passwordsInDB = db.get(username) # returns single password delimeted with '\x00'
                    if passwordsInDB:
                        # passwordsInDB = pyshoco.decompress(passwordsInDB).encode()
                        passwordsInDB = passwordsInDB.split(b'\x00')
                        if password in passwordsInDB: # skip if password already in DB
                            skipCount += 1
                            continue
                        passwordsInDB.append(password)
                        buffer[username] = passwordsInDB
                        batch.delete(username) # mark old record for deletion, as new record has been added to buffer and will be written later
                    else:
                        buffer[username] = [password]
                successCount += 1

            batchCount += 1
            if batchCount % batchBlocks == 0:
                for username, passwords in buffer.items():
                    batch.put(username, b'\x00'.join(passwords))
                buffer = {}
                batch.write()
                batch.clear()

        for username, passwords in buffer.items():
            batch.put(username, b'\x00'.join(passwords))
            # batch.put(username, pyshoco.compress(b'\x01'.join(passwords)))
        buffer = {}
        batch.write()
        batch.clear()

    totalSuccess += successCount
    totalSkipped += skipCount
    processedCount = successCount + skipCount
    totalProcessed += processedCount
    duration = time.time() - startTime
    totalDuration += duration
    print('[{}] Took {:.2f}s, {:.2f} creds/s, {}/{} creds indexed.'.format(archive, duration, processedCount / duration, successCount, processedCount))

db.close()
print('[+] Done! Total duration {:.2f}s, {:.2f} avg creds/s, {} total processed creds, {} total new creds indexed.'.format(totalDuration, totalProcessed / totalDuration, totalProcessed, totalSuccess))


