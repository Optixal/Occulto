#!/usr/bin/env python3

import sys
import plyvel
import zstandard as zstd
import replacer
import time

if len(sys.argv) < 2:
    print('Usage: {} archive [archive2] ...'.format(sys.argv[0]))
    exit(1)

dbLocation = '/home/optixal/Documents/github/Occulto/TestDB/'
db = plyvel.DB(dbLocation, create_if_missing=True)
decompressor = zstd.ZstdDecompressor()
batch = db.write_batch()

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
                    print('[-] Could not parse: {}'.format(cred))
                    skipCount += 1
                    continue
                if not password or len(password) > 512:
                    print('[-] Skipping, empty or too long: {}'.format(cred))
                    skipCount += 1
                    continue

                username = username.lower() # assumes all usernames/emails are case insensitive
                username = replacer.compress(username)

                passwords = db.get(username)
                if passwords:
                    passwords = passwords.split(b'\x00')
                    if password in passwords:
                        skipCount += 1
                        continue
                    passwords.append(password)
                    passwords = b'\x00'.join(passwords)
                    # passwords += b'\x00' + password
                    batch.delete(username)
                else:
                    passwords = password
                batch.put(username, passwords)
                # print(username, password)
                successCount += 1

            batchCount += 1
            if batchCount % batchBlocks == 0:
                batch.write()
                batch.clear()

        batch.write()
        batch.clear()

    totalSuccess += successCount
    totalSkipped += skipCount
    processedCount = successCount + skipCount
    totalProcessed = processedCount
    duration = time.time() - startTime
    totalDuration += duration
    print('[{}] Took {:.2f}s, {:.2f} creds/s, {}/{} creds indexed.'.format(archive, duration, processedCount / duration, successCount, processedCount))

db.close()
print('[+] Done! Total duration {:.2f}s, {:.2f} avg creds/s, {} total processed creds, {} total new creds indexed.'.format(totalDuration, totalProcessed / totalDuration, totalProcessed, totalSuccess))


