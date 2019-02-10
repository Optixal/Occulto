#!/usr/bin/env python3

import sys
import plyvel
import replacer

if len(sys.argv) < 2:
    print('Usage: {} alias [alias2] ...'.format(sys.argv[0]))
    exit(1)

dbLocation = '/home/optixal/Documents/github/Occulto/TestDB/'
db = plyvel.DB(dbLocation, create_if_missing=False)

for username in sys.argv[1:]:

    username = username.lower().encode()
    usernameOrig = username
    username = replacer.compress(username)
    passwords = db.get(username)
    if not passwords: continue
    passwords = passwords.split(b'\x00')
    for password in passwords:
        print(usernameOrig + b':' + password)

db.close()

