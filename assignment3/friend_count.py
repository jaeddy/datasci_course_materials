import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # key: person
    # value: count of friend
    key = record[0]
    value = 1
    mr.emit_intermediate(key, value)    

# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: order id
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
        total += v
    mr.emit((key, total))
        
# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)