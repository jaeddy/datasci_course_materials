import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # key: sequence id
    # value: nucleotides
    key = record[0]
    value = record[1]
    trim_seq = value[:-10]
    
    mr.emit_intermediate(trim_seq, 1)

# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: sequence
    # value: list of occurrence counts
    mr.emit(key)

# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)