#!/usr/bin/env python3

import plyvel

dbMetaLocation = '/home/optixal/Documents/github/Occulto/MetaDB'
dbMeta = plyvel.DB(dbMetaLocation, create_if_missing=True)
for key, value in dbMeta:
    print(key, value)
