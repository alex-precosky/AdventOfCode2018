import copy
from heapq import heappush, heappop
import queue
import re

class Node:

    def __init__(self, letter):
        self.letter = letter
        self.children = []

    def __repr__(self):
        return f'node:{self.letter}'

    def __lt__(self, other):
        return(self.letter < other.letter)

class Worker:
    def __init__(self):
        self.time_left = 0
        self.work_item = Node('-')

def get_next_work_item(heap, remaining, finished):
    # pop items til we get one that is available
    is_available = False
    while not is_available:
        put_back = []
        node = heappop(heap)

        is_available = True
        for letter, letter_node in remaining.items():
            if node in letter_node.children and letter_node is not node:
                is_available = False
            
        if not is_available:
            put_back.append(node)
        else:
            del remaining[node.letter]
            finished.append(node)
            for item in put_back:
                if item not in heap:
                    heappush(heap, item)

    for child in node.children:
        if child not in finished and child not in heap:
            heappush(heap, child)
        
    return node, heap, remaining, finished


def priority_graph_traversal(graph_heads, graph_dict, num_workers=1):
    heap = []
    steps = []

    for head in graph_heads:
        heappush(heap, head)

    remaining = graph_dict
    finished = []

    available_worker_queue = queue.Queue()

    for i in range(num_workers):
        available_worker_queue.put(Worker())

    working_workers = []
    total_time = 0

    while len(remaining) != 0 or len(working_workers) != 0:

        total_time += 1

        if(not available_worker_queue.empty()):
            worker = available_worker_queue.get()
            work_item, heap, remaining, finished = get_next_work_item(heap, remaining, finished)
            worker.time_left = ord(work_item.letter)-4
            worker.work_item = work_item
            working_workers.append(worker)


        for worker in working_workers:
            worker.time_left -= 1
            if worker.time_left == 0:
                steps.append(worker.work_item.letter)
                available_worker_queue.put(worker)
                working_workers.remove(worker)

    print(total_time)
    return ''.join(steps)

def get_letters_from_line(line):
    match = re.search(r'(?<=Step )([A-Z])', line)
    first_letter = match.group(0)
    match = re.search(r'(?<=step )([A-Z])', line)
    second_letter = match.group(0)

    return first_letter, second_letter

def main():

    # find the letter in first_letters that isn't in second_letters to find the head node
    graph_dict = {}
    first_letters = set()
    second_letters = set()

    for line in open('input/Day7.txt').readlines():
        first_letter, second_letter = get_letters_from_line(line.strip())

        first_letters.add(first_letter)
        second_letters.add(second_letter)

        if first_letter not in graph_dict:
            graph_dict[first_letter] = Node(first_letter)
          
        if second_letter not in graph_dict:
            graph_dict[second_letter] = Node(second_letter)

        graph_dict[first_letter].children.append(graph_dict[second_letter])
    
    
    first_letters.difference_update(second_letters)
    graph_heads = []
    for letter in first_letters:
        graph_heads.append(graph_dict[letter])

    part1_order = priority_graph_traversal(graph_heads, graph_dict, num_workers=1)
    print(part1_order)

    part2_order = priority_graph_traversal(graph_heads, graph_dict, num_workers=5)
    print(part2_order)

if __name__ == "__main__":
    main()
