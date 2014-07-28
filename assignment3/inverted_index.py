import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    
    # Only emit if unique word
    unique_words = []
    for w in words:
        if w not in unique_words:
            unique_words.append(w)
            mr.emit_intermediate(w, key)

# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: word
    # value: list of document ids
    mr.emit((key, list_of_values))

# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)