#!/usr/bin/env python3

import xxhash

def xxhashsum(filename, size=1024):
    h  = xxhash.xxh64()
    b  = bytearray(size)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

if __name__ == '__main__':
    import time
    for multi in [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]:
        start = time.time()
        # print(timeit.timeit('xxhashsum("1 (58).txt.zst", multi * 1024)', number=1000, globals=globals()))
        print(xxhashsum("1 (58).txt.zst", multi * 1024))
        print(multi, time.time() - start)

