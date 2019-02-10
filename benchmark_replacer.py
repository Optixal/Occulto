#!/usr/bin/env python3
import timeit
import re
from functools import reduce

email = b'test@live.com.sg'
# email = b'live.com@live.com'
# email = b'live.com'
# email = b'\x02'
# email = b'test@alive.com.sag'

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

replacementsItems = replacements.items()
backup = replacements
backup2 = replacementsItems

inverseReplacements = {v: k for k, v in replacements.items()}
inverseReplacementsItems = inverseReplacements.items()

# Test 1
def replaceAll(text, tup):
    for k, v in tup:
        text = text.replace(k, v)
    return text
duration = timeit.timeit('replaceAll(email, replacementsItems)', number=10000, globals=globals())
print(f'Test 1 - Replace For Loop: Time taken: {duration:.5f} sec')
print(replaceAll(email, replacementsItems))

# Test 2
rep = dict((re.escape(k), v) for k, v in replacementsItems)
pattern = re.compile(b'|'.join(rep.keys()))
def reSub(text):
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
duration = timeit.timeit('reSub(email)', number=10000, globals=globals())
print(f'Test 2 - Regex Sub: Time taken: {duration:.5f} sec')
print(reSub(email))

# Test 3
def reduction(text):
    return reduce(lambda a, kv: a.replace(*kv), replacementsItems, text)
duration = timeit.timeit('reduction(email)', number=10000, globals=globals())
print(f'Test 3 - Reduce: Time taken: {duration:.5f} sec')
print(reduction(email))

# Test 4
# Place longer ones first to keep shorter substrings from matching where the longer ones should take place
# For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
# 'hey ABC' and not 'hey ABc'
substrs = sorted(replacements, key=len, reverse=True)
# Create a big OR regex that matches any of the substrings to replace
# regexp = re.compile(b'|'.join(map(re.escape, replacements.keys())))
regexp = re.compile(b'(@)(' + b'|'.join(map(re.escape, substrs)) + b')$')
def reSubOptimized(text):
    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: b'@' + replacements[match.group(2)], text)
duration = timeit.timeit('reSubOptimized(email)', number=10000, globals=globals())
print(f'Test 4 - Regex Sub Optimized: Time taken: {duration:.5f} sec')
replaced = reSubOptimized(email)
print(replaced)

# Test 5
substrs = sorted(inverseReplacements, key=len, reverse=True)
# regexp = re.compile(b'|'.join(map(re.escape, substrs)))
regexp = re.compile(b'(@)(' + b'|'.join(map(re.escape, substrs)) + b')$')
def inverseReSubOptimized(text):
    # return regexp.sub(lambda match: inverseReplacements[match.group(0)], text)
    return regexp.sub(lambda match: b'@' + inverseReplacements[match.group(2)], text)
duration = timeit.timeit('inverseReSubOptimized(replaced)', number=10000, globals=globals())
print(f'Test 5 - Inverse Regex Sub Optimized: Time taken: {duration:.5f} sec')
print(inverseReSubOptimized(replaced))

print('\nCheck:')
print(replacements == backup)
print(replacementsItems == backup2)
