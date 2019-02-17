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

chunkSize = 1024 * 128
# chunksPerBatch = 2048

dbMetaLocation = '/home/optixal/Documents/github/Occulto/MetaDB'

archive = '/home/optixal/Documents/github/Occulto/1 (58).txt.zst'


db = plyvel.DB(dbLocation, create_if_missing=True)
# batch = db.write_batch(transaction=True)
decompressor = zstd.ZstdDecompressor()

totalSuccess = 0
totalSkipped = 0
totalProcessed = 0
totalDuration = 0

successCount = 0
skipCount = 0
processedCount = 0
chunkCount = 0
# batchCount = 0
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

            passwordsInDB = db.get(username) # returns single password delimeted with '\x00'
            if passwordsInDB:
                passwordsInDB = passwordsInDB.split(b'\x00')
                if password in passwordsInDB: # skip if password alr    skipCount += 1
                    continue
                passwordsInDB.append(password)
                db.delete(username) # mark old record for deletion, as new record has been added to buffer and will be written later
                db.put(username, b'\x00'.join(passwordsInDB))
            else:
                db.put(username, password)
            successCount += 1

        chunkCount += 1

totalSuccess += successCount
totalSkipped += skipCount
processedCount = successCount + skipCount
totalProcessed += processedCount
duration = time.time() - startTime
totalDuration += duration
# print('[{}] Took {:.2f}s, {:.2f} creds/s, {}/{} creds indexed.'.format(archive, duration, processedCount / duration, successCount, processedCount))

print('[+] Total duration {:.2f}s, {:.2f} avg creds/s, {} total processed creds, {} total new creds indexed.'.format(totalDuration, totalProcessed / totalDuration, totalProcessed, totalSuccess))
db.close()
shutil.rmtree(dbLocation)


