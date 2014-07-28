import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # mat: matrix name
    # row: row number
    # col: column number
    # val: value
    mat = record[0]
    row = record[1]
    col = record[2]
    val = record[3]
    
    # Hard-code matrix dims, a: LxM and b: MxN
    L = 5
    M = 5
    N = 5
    
    # Emit elements of each matrix to elements of the output product matrix
    if mat == "a":
        i = row
        j = col
        for k in range(N):
            mr.emit_intermediate((i, k), [mat, j, val])
        
    if mat == "b":
        j = row
        k = col
        for i in range(L):
            mr.emit_intermediate((i, k), [mat, j, val])
    
    
# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: output product matrix element (i, k)
    # value: list of matrix elements a(i, j) and b(j, k)
    
    # create temporary lists for elements of each matrix
    a_elements = []
    b_elements = []
    for v in list_of_values:
        if v[0] == "a":
            a_elements.append(v)
        else:
            b_elements.append(v)
    
    out_elements = []
    for a_elem in a_elements:
        for b_elem in b_elements:
            if a_elem[1] == b_elem[1]:
                out_elements.append(a_elem[2] * b_elem[2])
    mr.emit(key + (sum(out_elements),))

# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)