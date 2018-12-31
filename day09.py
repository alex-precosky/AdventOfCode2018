"""Advent of Code 2018: Day 9"""
from collections import defaultdict
import ipdb

class Marble:
    """Doubly linked list node"""
    def __init__(self, number):
        self.number = number
        self.next = self
        self.prev = self


class Circle:
    """Doubly linked circular list"""
    def __init__(self, marble):
        self.root = marble
        self.current_marble = self.root

    def insert(self, marble):
        """Inserts after one marble clockwise from current marble"""
        node = self.current_marble
        node = node.next
        if node.next is self.root:
            node.next = marble
            marble.prev = node
            marble.next = self.root
            self.root.prev = marble
        else:
            temp = node.next
            node.next = marble
            marble.next = temp
            marble.prev = node
            temp.prev = marble

        self.current_marble = marble

    def remove(self):
        """Removes marble 7 counter-clockwise from current and is returned
        Marble clockwise of the removed one is the new current marble"""
        node = self.current_marble
        for i in range(7):
            node = node.prev

        return_node = node
        node.prev.next = return_node.next
        return_node.next.prev = node.prev
        self.current_marble = return_node.next

        return_node.next = None
        return_node.prev = None

        return return_node

    def __repr__(self):
        node = self.root

        return_str = ""

        while True:
            if node is self.current_marble:
                return_str += f"({node.number}) "
            else:
                return_str += f" {node.number}  "
            node = node.next
            if node is self.root:
                break

        return return_str

def play_game(num_players, last_marble):
    """Returns winning score"""
    scores = defaultdict(int)

    root_marble = Marble(0)
    circle = Circle(root_marble)

    i = 1
    cur_player = i
    while True:

        if i % 23 != 0:
            circle.insert(Marble(i))
        else:
            removed_marble = circle.remove()

            scores[cur_player] += i
            scores[cur_player] += removed_marble.number

        i += 1
        cur_player = (cur_player + 1) % (num_players + 1)
        if cur_player == 0:
            cur_player = 1

        if i == last_marble:
            break

    max_score = max(scores.values())
    return max_score

def main():

    num_players = 463
    last_marble = 71787
    part_1_max_score = play_game(num_players, last_marble)
    print(f'Part 1 max score: {part_1_max_score}')

    last_marble *= 100
    part_2_max_score = play_game(num_players, last_marble)
    print(f'Part 2 max score: {part_2_max_score}')

if __name__ == "__main__":
    main()
