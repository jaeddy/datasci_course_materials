import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # key: person
    # value: friend
    key = record[0]
    value = record[1]

    mr.emit_intermediate((key, value), 1)
    mr.emit_intermediate((value, key), 1)

# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: person-friend pair
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
        total += v
    if total != 2:
        mr.emit(key)
        
# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)