import itertools
import math
import threading

def calculate_combinations(password_length, characterset):
    return len(characterset) ** int(password_length)

def calculate_passwords_per_core(total_combinations, number_of_cores):
    return math.floor(total_combinations / number_of_cores)

def calculate_keyspace(core_number, total_combinations, number_of_cores, percore):
    range_end = math.floor(((total_combinations / number_of_cores) * core_number))
    range_start = math.floor(range_end - percore)
    print("Core " + str(core_number) + ": " + str(range_start) + " - " + str(range_end))
    return [range_start, range_end]

def get_keyspace_start_end(keyspace_start_pos, keyspace_end_pos, characterset, password_length, total_combinations):
    attemptno = 0
    ranges =  []
    for attempt in itertools.product(characterset, repeat=password_length):
        if attemptno == keyspace_start_pos:
            ranges.append(''.join(attempt))
            print("Range start: " + ''.join(attempt))
        elif attemptno == keyspace_end_pos:
            ranges.append(''.join(attempt))
            print("Range end: " + ''.join(attempt))
            return ranges
        elif attemptno == (keyspace_end_pos - 1) and attemptno + 1 == total_combinations:
            ranges.append(''.join(attempt))
            print("Range end: " + ''.join(attempt))
            return ranges
        attemptno += 1

def do_everything(total_combinations, number_of_cores, percore, charset, password_length):
    threads = []
    # First calculate the keyspace_start and end (for each thread)
    for i in range(1, number_of_cores + 1):
        keyspace = calculate_keyspace(i, total_combinations, number_of_cores, percore)
        threads.append(threading.Thread(target=get_keyspace_start_end, args=(int(keyspace[0]), int(keyspace[1]), charset, int(password_length), total_combinations)))
    for thread in threads:
        thread.start()
        # TODO: Find a way to retrieve the keyspace_start and end from the threads
        # Start the dang cracking!
        # NOTE: These threads will use the previously calculated keyspace_start and end

def start_cracking():
    pass