import copy
import queue

def recursive_read_1(num_queue):

    num_children = num_queue.get()
    num_metadata_entries = num_queue.get()

    metadata_sum = 0

    for i in range(num_children):
        metadata_sum += recursive_read_1(num_queue)


    for i in range(num_metadata_entries):
        metadata_sum += num_queue.get()

    return metadata_sum

def recursive_read_2(num_queue):

    num_children = num_queue.get()
    num_metadata_entries = num_queue.get()

    child_node_values = [0] * num_children
    for i in range(num_children):
        child_node_values[i] = recursive_read_2(num_queue)

    
    metadata_values = [0] * num_metadata_entries

    for i in range(num_metadata_entries):
        metadata_values[i] = num_queue.get()


    node_value = 0

    if num_children == 0:
        for value in metadata_values:
            node_value += value
    else:
        for child in metadata_values:
            if child <= num_children:
                node_value += child_node_values[child-1] # -1 because file uses 1-based indexing

    return node_value


def main():
    in_file = open('input/Day8.txt')
    tokens = in_file.readline().split()

    num_queue = queue.Queue()

    for token in tokens:
        num_queue.put(int(token))
    
    metadata_sum = recursive_read_1(num_queue)
    print(f'Part 1 metadata sum: {metadata_sum}')

    for token in tokens:
        num_queue.put(int(token))

    node_value = recursive_read_2(num_queue)
    print(f'Part 2 node value: {node_value}')

    

if __name__ == "__main__":
    main()
