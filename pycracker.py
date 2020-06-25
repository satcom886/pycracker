#!/usr/bin/python
# Usage: pycracker.py MAXPASSWORDLENGTH HASH CHARACTERS HASHTYPE

# Import required modules
import hashlib
import sys
import itertools
import string
from tqdm import tqdm
import math

def figure_out_charset(characters):
    # Maybe this could be done a bit better?
    # This determines what character set should be used and calculates the number of possible combinations

    if "a" in characters and "A" not in characters and "1" not in characters and "@" not in characters:
        charset = string.ascii_lowercase
    
    elif "a" in characters and "A" in characters and "1" not in characters and "@" not in characters:
        charset = string.ascii_letters
    
    elif "a" in characters and "A" in characters and "1" in characters and "@" not in characters:
        charset = string.ascii_letters + string.digits
    
    elif "a" not in characters and "A" in characters and "1" in characters and "@" not in characters:
        charset = string.ascii_uppercase + string.digits
    
    elif "a" not in characters and "A" not in characters and "1" in characters and "@" not in characters:
        charset = string.digits
    
    elif "a" in characters and "A" not in characters and "1" in characters and "@" not in characters:
        charset = string.ascii_lowercase + string.digits
    
    elif "a" not in characters and "A" in characters and "1" not in characters and "@" not in characters:
        charset = string.ascii_uppercase
    
    elif "a" in characters and "A" in characters and "1" in characters and "@" in characters:
        charset = string.printable
    
    elif "a" in characters and "A" not in characters and "1" not in characters and "@" in characters:
        charset = string.ascii_lowercase + string.punctuation
    
    elif "a" not in characters and "A" in characters and "1" not in characters and "@" in characters:
        charset = string.ascii_uppercase + string.punctuation
    
    elif "a" not in characters and "A" not in characters and "1" in characters and "@" in characters:
        charset = string.digits + string.punctuation
    
    elif "a" in characters and "A" in characters and "1" not in characters and "@" in characters:
        charset = string.ascii_letters + string.punctuation
    
    elif "a" in characters and "A" not in characters and "1" in characters and "@" in characters:
        charset = string.ascii_lowercase + string.digits + string.punctuation
    
    elif "a" not in characters and "A" in characters and "1" in characters and "@" in characters:
        characters = string.ascii_uppercase + string.digits + string.punctuation
    
    charset_and_possiblecombinations = [charset, len(charset) ** int(sys.argv[-4])]
    print("Possible combinations:", charset_and_possiblecombinations[1])
    print("Characterset:", charset_and_possiblecombinations[0])
    return charset_and_possiblecombinations

# From https://stackoverflow.com/a/48389007
# Returns the password in plaintext
def solve_md5(userhash, maxlen, charset, possiblecombinations):
    print("Starting to crack a MD5 hash...")
    print("Please be patient!")
    hash_cracked = False
    attemptno = 0
    # Calculating stuff
    for i in range(maxlen+1):
        for attempt in tqdm(itertools.product(charset, repeat=i)):
            # print(''.join(attempt)) # Uncomment in order to print the current candidate
            attemptno += 1
            if hashlib.md5(''.join(attempt).encode('utf-8')).hexdigest() == userhash:
                hash_cracked = True
                print("\n\nHash cracked!")
                print(hashlib.md5(''.join(attempt).encode('utf-8')).hexdigest(), "-", ''.join(attempt),"\n")
                return ''.join(attempt)
            elif hash_cracked is False and attemptno == possiblecombinations:
                print("\n\nI tried", possiblecombinations, "different passwords and none of them worked")
                print("Hash not found :(")
                print(userhash, "- ???\n")
                return None

# charset_and_possiblecombinations = figure_out_charset(sys.argv[-2])
# solve_md5(sys.argv[-3], int(sys.argv[-4]), charset_and_possiblecombinations[0], int(charset_and_possiblecombinations[1]))


passlen = 4
charset = string.ascii_letters + string.digits
combinations = len(charset) ** int(passlen)
numcores = 2
percore = math.floor(combinations / numcores)

print("Characer set: " + charset)
print("Total combinations: " + str(combinations))
print("Iterarions per core: " + str(percore))
for coreno in range(1, numcores + 1):
    range_end = math.floor(((combinations / numcores) * coreno))
    range_start = math.floor(range_end - percore)
    print(str(coreno) + ": " + str(range_start) + " - " + str(range_end))
print("Now calculating the ranges...")
# Here the range is calculated (000 - 250 with 4 cores)
for coreno in range(1, numcores + 1):
    range_end = math.floor(((combinations / numcores) * coreno))
    range_start = math.floor(range_end - percore)
    attemptno = 0
    for attempt in itertools.product(charset, repeat=passlen):
        if attemptno == range_start:
            print("Core " + str(coreno) + ": " + ''.join(attempt), end=" - ")
        elif attemptno == range_end:
            print(''.join(attempt))
        elif attemptno == (range_end - 1) and attemptno + 1 == combinations:
            print(''.join(attempt))
        attemptno += 1
