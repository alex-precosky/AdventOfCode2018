"""Advent of Code 2018: Day 7"""
import copy
from heapq import heappush, heappop
import ipdb
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

def get_next_work_item(heap, remaining, in_progress, finished):

    # pop items til we get one that is available
    is_available = False
    put_back = []
    node = None

    while not is_available and len(heap) > 0:
        put_back = []
        node = heappop(heap)

        is_available = True
        for letter, letter_node in remaining.items():
            if node in letter_node.children and letter_node is not node:
                is_available = False

        for letter, letter_node in in_progress.items():
            if node in letter_node.children and letter_node is not node:
                is_available = False
            
        if not is_available:
            put_back.append(node)
            node = None
        else:
            del remaining[node.letter]
            in_progress[node.letter] = node
        
    for item in put_back:
        if item not in heap:
            heappush(heap, item)
        
    return node, heap, remaining, in_progress, finished


def priority_graph_traversal(graph_heads, graph_dict, num_workers=1):
    heap = []
    steps = []

    for head in graph_heads:
        heappush(heap, head)

    remaining = graph_dict
    in_progress = {}
    finished = []

    available_worker_queue = queue.Queue()

    for i in range(num_workers):
        available_worker_queue.put(Worker())

    working_workers = []
    total_time = 0

    while len(remaining) != 0 or len(working_workers) != 0:

        total_time += 1

        # assign work to workers as long as there is work and workers available
        while (not available_worker_queue.empty()):
            work_item, heap, remaining, in_progress, finished = get_next_work_item(heap, remaining, in_progress, finished)

            if work_item is not None:
                worker = available_worker_queue.get()
                worker.time_left = ord(work_item.letter)-4
                worker.work_item = work_item
                working_workers.append(worker)
            else:
                break


        for worker in working_workers:
            worker.time_left -= 1
            if worker.time_left == 0:
                steps.append(worker.work_item.letter)
                available_worker_queue.put(worker)

                del in_progress[worker.work_item.letter]

                for child in worker.work_item.children:
                    if child not in finished and child not in heap:
                        heappush(heap, child)

        working_workers = [worker for worker in working_workers if worker.time_left != 0]

    return ''.join(steps), total_time

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

    part1_order, part1_time = priority_graph_traversal(graph_heads, dict(graph_dict), num_workers=1)
    print(f'Order: {part1_order} Time: {part1_time} s')

    part2_order, part2_time = priority_graph_traversal(graph_heads, dict(graph_dict), num_workers=5)
    print(f'Order: {part2_order} Time: {part2_time} s')

if __name__ == "__main__":
    main()

