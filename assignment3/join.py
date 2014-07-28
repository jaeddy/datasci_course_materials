import sys
import MapReduce

# Part 1: Create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: Mapper function
def mapper(record):
    # key: order id
    # value: table identifier
    key = record[1]
    value = record[0]
    mr.emit_intermediate(key, record)    

# Part 3: Reducer function
def reducer(key, list_of_values):
    # key: order id
    # value: list of records
    
    # create temporary lists for order and line_item records
    order_records = []
    lineitem_records = []
    for record in list_of_values:
        if record[0] == "order":
            order_records.append(record)
        else:
            lineitem_records.append(record)
    
    # for each order, join records for all order-line_item combinations
    for order in order_records:
        for lineitem in lineitem_records:
            mr.emit(order[0:len(order)] + lineitem)
        
# Part 4: Execute code
if __name__ == '__main__':
    INPUT_DATA = open(sys.argv[1])
    mr.execute(INPUT_DATA, mapper, reducer)