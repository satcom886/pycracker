# Import required modules
import hashlib
import sys
import string
import psutil
import argparse
import threading

import pycracker.bruteforce

# From https://stackoverflow.com/a/48389007
# Returns the password in plaintext
def solve_md5(userhash, maxlen, charset, possiblecombinations):
    print("Starting to crack a MD5 hash...")
    print("Please be patient!")
    hash_cracked = False
    attemptno = 0
    # Calculating stuff
    for i in range(maxlen+1):
        for attempt in itertools.product(charset, repeat=i):
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

def calculate_password_ranges(keyspace_start, keyspace_end, characterset, password_length, total_combinations):
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

def print_info():
    print("Characer set: " + characterset)
    print("Total combinations: " + str(total_combinations))
    print("Iterations per core: " + str(percore))
    print("Number of detected cores: " + str(number_of_cores))

# Variables for testing
# print(pycracker.bruteforce.get_keyspace_start_end(0, 1000, string.ascii_letters, 4, pycracker.bruteforce.calculate_keyspace(4, string.ascii_letters)))

def get_arguments():
    ap = argparse.ArgumentParser()
    # Add the arguments to the parser
    ap.add_argument("-a", "--attack-mode", required=True,
    help="Attack mode to use")
    ap.add_argument("-H", "--hash", required=False,
    help="Hash that we should attempt to crack")
    ap.add_argument("-f", "--hashlist", required=False,
    help="Hashlist file that we should attempt to crack")
    ap.add_argument("-m", "--hash-mode", required=True,
    help="Type of hash")
    ap.add_argument("-l", "--password-length", required=True,
    help="Number of characters in the password")
    ap.add_argument("-c", "--characterset", required=False,
    help="What characters should be used (bruteforce only)")
    ap.add_argument("--keyspace-start-pos", required=False,
    help="Keyspace start position")
    ap.add_argument("--keyspace-end-pos", required=False,
    help="Keyspace end position")
    ap.add_argument("--keyspace", required=False,
    help="Only calculate the keyspace")
    return vars(ap.parse_args())

arguments = get_arguments()
number_of_cores = psutil.cpu_count(logical = True)
if arguments["attack_mode"] == "bf":
    password_length = arguments["password_length"]
    charset = string.ascii_letters
    if arguments["hash_mode"] == "0":
        if arguments["keyspace_start_pos"] is not None and arguments["keyspace_stop_pos"] is not None:
            # TODO
            pass
        else:
            total_combinations = pycracker.bruteforce.calculate_combinations(password_length, charset)
            percore = pycracker.bruteforce.calculate_passwords_per_core(total_combinations, number_of_cores)
            pycracker.bruteforce.do_everything(total_combinations, number_of_cores, percore, charset, password_length)
