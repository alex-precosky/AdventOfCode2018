from heapq import heappush, heappop
import re

class Node:

    def __init__(self, letter):
        self.letter = letter
        self.children = []

    def __repr__(self):
        return f'node:{self.letter}'

    def __lt__(self, other):
        return(self.letter < other.letter)


def priority_graph_traversal(graph_heads, graph_dict):
    heap = []
    steps = []

    for head in graph_heads:
        print(f'Pushing {head}')
        heappush(heap, head)

    closed = graph_dict
    finished = []

    while len(heap) != 0:

        # pop items til we get one that is available
        is_available = False
        while not is_available:
            put_back = []
            node = heappop(heap)
            print(f'Popped {node}')

            is_available = True
            for letter, letter_node in closed.items():
                print(f'Checking child {letter_node}')
                if node in letter_node.children and letter_node is not node:
                    is_available = False
            
            if not is_available:
                print(f'queueing {node.letter} for putback')
                put_back.append(node)
            else:
                del closed[node.letter]
                finished.append(node)
                print(f'Closed {node.letter}')
                for item in put_back:
                    print(f'Putting back {item}')
                    if item not in heap:
                        heappush(heap, item)

        for child in node.children:
            if child not in finished and child not in heap:
                heappush(heap, child)

        steps.append(node.letter)

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

    print(graph_heads)
    print(graph_dict)
    answer = priority_graph_traversal(graph_heads, graph_dict)

    print(answer)

if __name__ == "__main__":
    main()
