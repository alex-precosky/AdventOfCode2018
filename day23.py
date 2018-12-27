import re
from z3 import *

def get_manhattan_distance(x1, y1, z1, x2, y2, z2):
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)

def z3abs(x):
    return If(x >= 0,x,-x)

def z3get_manhattan_distance(x1, y1, z1, x2, y2, z2):
    return z3abs(x2 - x1) + z3abs(y2 - y1) + z3abs(z2 - z1)

def get_manhattan_distance_nanobots(nanobot1, nanobot2):
    x1 = nanobot1.x
    y1 = nanobot1.y
    z1 = nanobot1.z

    x2 = nanobot2.x
    y2 = nanobot2.y
    z2 = nanobot2.z

    return get_manhattan_distance(x1, y1, z1, x2, y2, z2)

class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    @classmethod
    def from_str(self, input_str):
        pos_str = re.search("(?<=\<)[-\d.,]+(?=>)", input_str).group(0)

        pos_components = pos_str.split(',')
        x = int(pos_components[0])
        y = int(pos_components[1])
        z = int(pos_components[2])

        r_str = re.search("(?<=r\=)\d+", input_str).group(0)
        r = int(r_str)

        return Nanobot(x, y, z, r)

    def __repr__(self):
        return f'{self.x} {self.y} {self.z} {self.r}'

def main():
    nanobots = []

    for line in open('input/Day23.txt').readlines():
        nanobot = Nanobot.from_str(line.strip())
        nanobots.append(nanobot)

    # find strongest nanobot
    largest_range = 0
    strongest_nanobot = None
    for nanobot in nanobots:
        if nanobot.r > largest_range:
            largest_range = nanobot.r
            strongest_nanobot = nanobot

    print(f'Largest nanobot range is {largest_range}')

    # find how many nanobots are in range of it
    in_range_count = 0
    for nanobot in nanobots:
        distance = get_manhattan_distance_nanobots(nanobot, strongest_nanobot)
        if distance <= largest_range:
            in_range_count += 1

    print(f'Part 1: Nanobots in its range: {in_range_count}')

    # Part 2 uses z3 to solve an optimization problem: find the spot that is in the range
    # of as many nanobots as possible, choosing such a spot closest to 0,0,0 if there are multiple
    opt = Optimize()

    x, y, z = Ints('x y z')
    num_in_range = Int('num_in_range')
    dist_from_zero = Int('dist_from_zero')

    # Set up the number of nanobots in range of each nanobots, in terms of z3
    # variables
    in_ranges = []
    for i, nanobot in enumerate(nanobots):
        in_range = Int(f'in_range_{i}')
        in_ranges.append(in_range)
        opt.add(in_range == If(z3get_manhattan_distance(x, nanobot.x, y, nanobot.y,
                                                        z, nanobot.z) <= nanobot.r, 1, 0))
    opt.add(num_in_range == Sum(in_ranges))
    opt.add(dist_from_zero == z3abs(x) + z3abs(y) + z3abs(z))
    
    goal1 = opt.maximize(num_in_range)
    goal2 = opt.minimize(dist_from_zero)

    opt.check()
    print('Part 2: Lower and upper bounds of manhattan distance to optimum position:', opt.lower(goal2), opt.upper(goal2))

if __name__ == "__main__":
    main()
