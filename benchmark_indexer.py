#!/usr/bin/env python3

import sys
import plyvel
import zstandard as zstd
import replacer
import time
import pyshoco
import shutil

dbLocation = '/home/optixal/Documents/github/Occulto/TestDB/'
# db = plyvel.DB(dbLocation, create_if_missing=True)

chunkSizes = [1024, 1024 * 2, 1024 * 4, 1024 * 8, 1024 * 16, 1024 * 32, 1024 * 64, 1024 * 128]
chunksPerBatches = [128, 256, 512, 1024, 2048, 4096, 8192]

dbMetaLocation = '/home/optixal/Documents/github/Occulto/MetaDB'

archive = '/home/optixal/Documents/github/Occulto/1 (58).txt.zst'

for chunkSize in chunkSizes:
    for chunksPerBatch in chunksPerBatches:

        db = plyvel.DB(dbLocation, create_if_missing=True)
        batch = db.write_batch(transaction=True)
        decompressor = zstd.ZstdDecompressor()

        totalSuccess = 0
        totalSkipped = 0
        totalProcessed = 0
        totalDuration = 0

        successCount = 0
        skipCount = 0
        processedCount = 0
        chunkCount = 0
        batchCount = 0
        saved = None
        startTime = time.time()
        buffer = {}

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
                    if passwordsInBuffer: # db has already queried this email in this batch and results exists in buffer
                        if password in passwordsInBuffer: # skip if buffer already has password in it, as it is already going to be written
                            skipCount += 1
                            continue
                        buffer[username].append(password)
                    else:
                        passwordsInDB = db.get(username) # returns single password delimeted with '\x00'
                        if passwordsInDB:
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

                chunkCount += 1
                if chunkCount % chunksPerBatch == 0:
                    for username, passwords in buffer.items():
                        batch.put(username, b'\x00'.join(passwords))
                    buffer = {}
                    batch.write()
                    batch.clear()
                    batchCount += 1

            for username, passwords in buffer.items():
                batch.put(username, b'\x00'.join(passwords))
            buffer = {}
            batch.write()
            batch.clear()
            batchCount += 1

        totalSuccess += successCount
        totalSkipped += skipCount
        processedCount = successCount + skipCount
        totalProcessed += processedCount
        duration = time.time() - startTime
        totalDuration += duration
        # print('[{}] Took {:.2f}s, {:.2f} creds/s, {}/{} creds indexed.'.format(archive, duration, processedCount / duration, successCount, processedCount))

        print('[+] [{}] [{}] [{}] Total duration {:.2f}s, {:.2f} avg creds/s, {} total processed creds, {} total new creds indexed.'.format(chunkSize, chunksPerBatch, chunkSize * chunksPerBatch, totalDuration, totalProcessed / totalDuration, totalProcessed, totalSuccess))
        db.close()
        shutil.rmtree(dbLocation)


