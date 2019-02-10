#!/usr/bin/env python3
import timeit
import re
from functools import reduce

emails = [
    (b'test@live.com.sg', b'test@\x0b'),
    (b'live.com@live.com', b'live.com@\x61'),
    (b'live.com', b'live.com'),
    (b'\x02', b'\x02'),
    (b'test@alive.com.sga', b'test@alive.com.sga'),
]

replacements = {
    b'hotmail.com': b'\x02',
    b'yahoo.com': b'\x03',
    b'live.com': b'\x61',
    b'mail.com': b'\x05',
    b'msn.com': b'\x06',
    b'facebook.com': b'\x07',
    b'aol.com': b'\x08',
    b'googlemail.com1': b'\x09',
    b'googlemail.com2': b'\x09',
    b'googlemail.com3': b'\x09',
    b'googlemail.com4': b'\x09',
    b'googlemail.com5': b'\x09',
    b'googlemail.com6': b'\x09',
    b'googlemail.com7': b'\x09',
    b'googlemail.com8': b'\x09',
    b'googlemail.com9': b'\x09',
    b'googlemail.com10': b'\x09',
    b'googlemail.com11': b'\x09',
    b'googlemail.com12': b'\x09',
    b'googlemail.com13': b'\x09',
    b'googlemail.com14': b'\x09',
    b'googlemail.com15': b'\x09',
    b'googlemail.com16': b'\x09',
    b'googlemail.com17': b'\x09',
    b'googlemail.com18': b'\x09',
    b'googlemail.com19': b'\x09',
    b'googlemail.com20': b'\x09',
    b'googlemail.com21': b'\x09',
    b'googlemail.com22': b'\x09',
    b'googlemail.com23': b'\x09',
    b'googlemail.com24': b'\x09',
    b'googlemail.com25': b'\x09',
    b'googlemail.com26': b'\x09',
    b'googlemail.com27': b'\x09',
    b'googlemail.com28': b'\x09',
    b'googlemail.com29': b'\x09',
    b'googlemail.com30': b'\x09',
    b'googlemail.com31': b'\x09',
    b'googlemail.com32': b'\x09',
    b'googlemail.com33': b'\x09',
    b'googlemail.com34': b'\x09',
    b'googlemail.com35': b'\x09',
    b'googlemail.com36': b'\x09',
    b'googlemail.com37': b'\x09',
    b'googlemail.com38': b'\x09',
    b'googlemail.com39': b'\x09',
    b'googlemail.com40': b'\x09',
    b'googlemail.com41': b'\x09',
    b'googlemail.com42': b'\x09',
    b'googlemail.com43': b'\x09',
    b'googlemail.com44': b'\x09',
    b'googlemail.com45': b'\x09',
    b'googlemail.com46': b'\x09',
    b'googlemail.com47': b'\x09',
    b'googlemail.com48': b'\x09',
    b'googlemail.com49': b'\x09',
    b'googlemail.com50': b'\x09',
    b'googlemail.com51': b'\x09',
    b'googlemail.com52': b'\x09',
    b'googlemail.com53': b'\x09',
    b'googlemail.com54': b'\x09',
    b'googlemail.com55': b'\x09',
    b'googlemail.com56': b'\x09',
    b'googlemail.com57': b'\x09',
    b'googlemail.com58': b'\x09',
    b'googlemail.com59': b'\x09',
    b'googlemail.com60': b'\x09',
    b'googlemail.com61': b'\x09',
    b'googlemail.com62': b'\x09',
    b'googlemail.com63': b'\x09',
    b'googlemail.com64': b'\x09',
    b'googlemail.com65': b'\x09',
    b'googlemail.com66': b'\x09',
    b'googlemail.com67': b'\x09',
    b'googlemail.com68': b'\x09',
    b'googlemail.com69': b'\x09',
    b'googlemail.com70': b'\x09',
    b'googlemail.com71': b'\x09',
    b'googlemail.com72': b'\x09',
    b'googlemail.com73': b'\x09',
    b'googlemail.com74': b'\x09',
    b'googlemail.com75': b'\x09',
    b'googlemail.com76': b'\x09',
    b'googlemail.com77': b'\x09',
    b'googlemail.com78': b'\x09',
    b'googlemail.com79': b'\x09',
    b'googlemail.com80': b'\x09',
    b'googlemail.com81': b'\x09',
    b'googlemail.com82': b'\x09',
    b'googlemail.com83': b'\x09',
    b'googlemail.com84': b'\x09',
    b'googlemail.com85': b'\x09',
    b'googlemail.com86': b'\x09',
    b'googlemail.com87': b'\x09',
    b'googlemail.com88': b'\x09',
    b'googlemail.com89': b'\x09',
    b'googlemail.com90': b'\x09',
    b'googlemail.com91': b'\x09',
    b'googlemail.com92': b'\x09',
    b'googlemail.com93': b'\x09',
    b'googlemail.com94': b'\x09',
    b'googlemail.com95': b'\x09',
    b'googlemail.com96': b'\x09',
    b'googlemail.com97': b'\x09',
    b'googlemail.com98': b'\x09',
    b'googlemail.com99': b'\x09',
    b'googlemail.com100': b'\x09',
    b'googlemail.com101': b'\x09',
    b'googlemail.com102': b'\x09',
    b'googlemail.com103': b'\x09',
    b'live.com.sg': b'\x0B',
    b'gmail.com': b'\x01',
}

inverseReplacements = {v: k for k, v in replacements.items()}
backup = replacements
backup2 = inverseReplacements

# substrsReplacements = sorted(replacements, key=len, reverse=True)
# regexpReplacements = re.compile(b'(@)(' + b'|'.join(map(re.escape, substrsReplacements)) + b')$')
regexpReplacements = re.compile(b'(@)(' + b'|'.join(map(re.escape, replacements.keys())) + b')$')
def compress(text):
    return regexpReplacements.sub(lambda match: b'@' + replacements[match.group(2)], text)

# substrsInverse = sorted(inverseReplacements, key=len, reverse=True)
# regexpInverse = re.compile(b'(@)(' + b'|'.join(map(re.escape, substrsInverse)) + b')$')
regexpInverse = re.compile(b'(@)(' + b'|'.join(map(re.escape, inverseReplacements.keys())) + b')$')
def uncompress(text):
    return regexpInverse.sub(lambda match: b'@' + inverseReplacements[match.group(2)], text)

for email in emails:
    compressed = compress(email[0])
    uncompressed = uncompress(compressed)
    passed = compressed == email[1] and email[0] == uncompressed
    print('Test: {} ... Compressed={}, Uncompressed={}, Pass={}'.format(email[0], compressed, uncompressed, passed))
    assert(passed)

print('Integrity Checks...')
assert(replacements == backup)
assert(inverseReplacements == backup2)
print('All tests passed.')
