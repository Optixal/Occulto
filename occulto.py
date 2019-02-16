#!/usr/bin/env python3

import sys
import plyvel
import replacer
import pyshoco

if len(sys.argv) < 2:
    print('Usage: {} alias [alias2] ...'.format(sys.argv[0]))
    exit(1)

# dbLocation = '/home/optixal/Documents/github/Occulto/TestDB/'
dbLocation = '/home/optixal/Apps/Occulto/TestDB/'
db = plyvel.DB(dbLocation, create_if_missing=False)

def getPasswords(username, db):
    username = replacer.compress(username)
    username = pyshoco.compress(username)
    passwords = db.get(username)
    if not passwords: return []
    # passwords = pyshoco.decompress(passwords).encode()
    return passwords.split(b'\x00')

def printPasswords(username, passwords):
    for password in passwords:
        print(username + b':' + password)

for username in sys.argv[1:]:
    username = username.lower().encode()
    passwords = getPasswords(username, db)
    printPasswords(username, passwords)
    for domain in replacer.replacements:
        email = username + b'@' + domain
        passwords = getPasswords(email, db)
        printPasswords(email, passwords)

db.close()

