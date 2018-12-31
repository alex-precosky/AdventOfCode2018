"""Advent of Code 2018: Day 6"""
import re


class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __eq__(self, other):
        return(self.X == other.X and self.Y == other.Y)

    def __repr__(self):
        return f'{self.X}, {self.Y}'

    @classmethod
    def from_str(cls, input_str):
        match = re.search(r'(\d+), (\d+)', input_str)
        X = int(match.group(1))
        Y = int(match.group(2))

        return Point(X, Y)

class Rectangle:
    def __init__(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def __eq__(self, other):
        return(self.top == other.top and self.left == other.left and self.bottom
               == other.bottom and self.right == other.right)

    def __repr__(self):
        return f'T: {self.top} L: {self.left} B: {self.bottom} R: {self.right}'


def manhattan_distance_to_point(ptA, ptB):
    return abs(ptB.X-ptA.X) + abs(ptB.Y-ptA.Y)


def find_bounds(targets):
    """Returns a bounding rect of all targets"""
    minX = 9999999
    maxX = -9999999
    minY = 9999999
    maxY = -9999999

    for target in targets:
        if target.X > maxX:
            maxX = target.X
        if target.X < minX:
            minX = target.X
        if target.Y > maxY:
            maxY = target.Y
        if target.Y < minY:
            minY = target.Y

    return Rectangle(top=minY, left=minX, bottom=maxY, right=maxX)


def find_index_of_closest_target(targets, pt):
    """Returns -1 for equidistant to two targets"""
    min_distance = 9999999
    closest_index = -1

    for i, target in enumerate(targets):
        distance = manhattan_distance_to_point(target, pt)
        if distance == 0:
            closest_index = -1
            break
        elif distance < min_distance:
            min_distance = distance
            closest_index = i
        elif distance == min_distance:
            closest_index = -1  # equidistant to two targets

    return closest_index


def find_largest_area(targets, indices_of_infinite_area_targets):
    """Ignoring targets that have an infinite area, finds the area of the target with the largest area"""

    bounds = find_bounds(targets)

    # key: index of target. value: area so far
    areas = {}

    for i, target in enumerate(targets):
        areas[i] = 0

    for x in range(0, bounds.right+100):
        for y in range(0, bounds.bottom+100):
            closest_target_index = find_index_of_closest_target(targets, Point(x, y))
            if closest_target_index != -1 and (closest_target_index not in indices_of_infinite_area_targets):
                areas[closest_target_index] += 1

    max_area = -99999
    for i, area in areas.items():
        if area > max_area:
            max_area = area

    max_area += 1  # include location of the target itself

    return max_area


def find_indices_of_infinite_area_targets(targets):
    """patrols the perimeter and returns list of indices to targets that are found there"""

    infinite_target_indices = set()

    bounds = find_bounds(targets)

    # walk top and bottom edge
    for x in range(0, bounds.right+1):
        target = find_index_of_closest_target(targets, Point(x, -100000))
        if target != -1:
            infinite_target_indices.add(target)

        target = find_index_of_closest_target(targets, Point(x, bounds.bottom+1000000))
        if target != -1:
            infinite_target_indices.add(target)

    # walk left and right edge
    for y in range(0, bounds.bottom+1):
        target = find_index_of_closest_target(targets, Point(-100000, y))
        if target != -1:
            infinite_target_indices.add(target)

        target = find_index_of_closest_target(targets, Point(bounds.right+100000, y))
        if target != -1:
            infinite_target_indices.add(target)

    return infinite_target_indices


def find_safe_area(targets, safe_threshold):

    bounds = find_bounds(targets)

    safe_area = 0

    for x in range(0, bounds.right):
        for y in range(0, bounds.bottom):
            distance = 0

            for target in targets:
                distance += manhattan_distance_to_point(Point(x, y), target)

            if distance < safe_threshold:
                safe_area += 1

    return safe_area


def main():

    targets = []

    for line in open('input/Day6.txt').readlines():
        targets.append(Point.from_str(line.strip()))

    indices_of_infinite_area_targets = find_indices_of_infinite_area_targets(targets)

    # Part 1: Find the size of the largest are that isn't infinite
    largest_area = find_largest_area(targets, indices_of_infinite_area_targets)
    print(f'Part 1: Largest area: {largest_area}')

    # Part 2: Find the size of the region containing all locations with a total
    # distance to all given coordinates of less than 1000q0
    safe_threshold = 10000
    safe_area = find_safe_area(targets, safe_threshold)
    print(f'Part 2: Safe area: {safe_area}')


if __name__ == "__main__":
    main()
