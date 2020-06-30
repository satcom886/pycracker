#!/usr/bin/python
# Usage: pycracker.py MAXPASSWORDLENGTH HASH CHARACTERS HASHTYPE

# Import required modules
import hashlib
import sys
import itertools
import string
from tqdm import tqdm
import math
import psutil

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

def calculate_password_ranges(core_number, keyspace_start, keyspace_end):
    print("Now calculating the ranges...")
    attemptno = 0
    ranges =  []
    for attempt in itertools.product(characterset, repeat=password_length):
        if attemptno == keyspace_start:
            ranges.append(''.join(attempt))
        elif attemptno == keyspace_end:
            ranges.append(''.join(attempt))
            return ranges
        elif attemptno == (keyspace_end - 1) and attemptno + 1 == total_combinations:
            ranges.append(''.join(attempt))
            return ranges
        attemptno += 1

def calculate_keyspaces(core_number):
    range_end = math.floor(((total_combinations / number_of_cores) * core_number))
    range_start = math.floor(range_end - percore)
    print("Core " + str(core_number) + ": " + str(range_start) + " - " + str(range_end))
    return [range_start, range_end]

def print_info():
    print("Characer set: " + characterset)
    print("Total combinations: " + str(total_combinations))
    print("Iterarions per core: " + str(percore))
    print("Number of detected cores: " + str(number_of_cores))

def calculate_total_combinations():
    return len(characterset) ** int(password_length)

def calculate_passwords_per_core():
    return math.floor(total_combinations / number_of_cores)

# Variables for testing
mode = "bruteforce"
password_length = 4
characterset = string.ascii_letters

# Global variables
number_of_cores = psutil.cpu_count(logical = True)
total_combinations = calculate_total_combinations()
percore = calculate_passwords_per_core()

print_info()
for core_number in range(1, number_of_cores + 1):
    ranges = calculate_keyspaces(core_number)
    print(calculate_password_ranges(core_number, ranges[0], ranges[1]))
