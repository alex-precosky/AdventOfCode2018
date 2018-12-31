"""Advent of Code 2018: Day 3"""
import re
import numpy as np

class rectangle:
    def __init__(self, claim_id, left, top, width, height):
        self.claim_id = claim_id
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __eq__(self, other):
        if (self.claim_id == other.claim_id) and (self.left == other.left) and (self.top == other.top) and (self.width == other.width) and (self.height
                                                                     == other.height):
            return True
        else:
            return False

    @classmethod
    def from_str(self, rectangle_str):
        tok = re.split(' |,|x|:', rectangle_str)
        
        claim_id = int(re.search('(?<=#)\d+', tok[0]).group(0))

        left = int(tok[2])
        top = int(tok[3])
        width = int(tok[5])
        height = int(tok[6])

        new_rect = rectangle(claim_id, left, top, width, height)
        return new_rect
        
    def __repr__(self):
        return f'ID: {self.claim_id} L: {self.left} T: {self.top} W: {self.width} H: {self.height}'

def place_rectangle_on_fabric(the_rectangle, fabric):
    for i in range(the_rectangle.left, the_rectangle.left + the_rectangle.width):
        for j in range(the_rectangle.top, the_rectangle.top + the_rectangle.height):
            fabric[j, i] += 1

    return fabric

def count_overlap(fabric):
    overlap = 0

    for x in np.nditer(fabric):
        if x > 1:
            overlap += 1

    return overlap


def does_rect_overlap(the_rectangle, fabric):
    overlap = False

    for i in range(the_rectangle.left, the_rectangle.left + the_rectangle.width):
        for j in range(the_rectangle.top, the_rectangle.top + the_rectangle.height):
            if fabric[j, i] > 1:
                overlap = True

    return overlap

def main():
    FABRIC_SIZE = 1000

    fabric = np.zeros([FABRIC_SIZE, FABRIC_SIZE])

    rectangles = []
    for line in open("input/Day3.txt").readlines():
        rectangles.append(rectangle.from_str(line.strip()))

    for rect in rectangles:
        fabric = place_rectangle_on_fabric(rect, fabric)

    overlap_area = count_overlap(fabric)

    print(f'Overlap: {overlap_area}')

    claim_id_non_overlap = -1
    for rect in rectangles:
        if does_rect_overlap(rect, fabric) is False:
            claim_id_non_overlap = rect.claim_id
            break

    print(f'Claim ID with no overlap: {claim_id_non_overlap}')

if __name__ == "__main__":
    main()
