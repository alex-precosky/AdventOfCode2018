from enum import IntEnum
from heapq import heappush, heappop


class Tool(IntEnum):
    Climbing = 1
    Torch = 2
    Nothing = 3


class TerrainType(IntEnum):
    ROCKY = 1
    WET = 2
    NARROW = 3


class DFSNode:
    def __init__(self, x, y, tool, time):
        self.x = x
        self.y = y
        self.tool = tool
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.tool == other.tool and self.time == other.time

def get_geologic_index(x, y, cave_depth, geologic_indexes, erosion_levels):
    if (x, y) in geologic_indexes:
        return geologic_indexes[(x, y)]
    else:
        if y == 0:
            geologic_index = x * 16807
            geologic_indexes[(x, y)] = geologic_index
            return geologic_index
        elif x == 0:
            geologic_index = y * 48271
            geologic_indexes[(x, y)] = geologic_index
            return geologic_index
        else:
            erosion_level1 = get_erosion_level(
                x-1, y, cave_depth, geologic_indexes, erosion_levels)

            erosion_level2 = get_erosion_level(
                x, y-1, cave_depth, geologic_indexes, erosion_levels)

            geologic_index = erosion_level1 * erosion_level2
            geologic_indexes[(x, y)] = geologic_index
            return geologic_index


def get_erosion_level(x, y, cave_depth, geologic_indexes, erosion_levels):
    if (x, y) in erosion_levels:
        return erosion_levels[(x, y)]
    else:
        geologic_index = get_geologic_index(
            x, y, cave_depth, geologic_indexes, erosion_levels)

        erosion_level = (geologic_index + cave_depth) % 20183
        erosion_levels[(x, y)] = erosion_level
        return erosion_level


def get_terrain_type(x, y, cave_depth, geologic_indexes, erosion_levels):
    erosion_level = get_erosion_level(
        x, y, cave_depth, geologic_indexes, erosion_levels)

    if erosion_level % 3 == 0:
        terrain_type = TerrainType.ROCKY
    elif erosion_level % 3 == 1:
        terrain_type = TerrainType.WET
    else:
        terrain_type = TerrainType.NARROW

    return terrain_type


def is_terrain_compatible(terrain, tool):
    if terrain == TerrainType.ROCKY:
        if tool == Tool.Climbing or tool == Tool.Torch:
            return True
        else:
            return False
    elif terrain == TerrainType.WET:
        if tool == Tool.Climbing or tool == Tool.Nothing:
            return True
        else:
            return False
    else:
        if tool == Tool.Torch or tool == Tool.Nothing:
            return True
        else:
            return False


def get_minimum_time_bfs(target, cave_depth, geologic_indexes, erosion_levels):
    open_queue = []

    visited = set()

    # time, x, y, tool
    heappush(open_queue, DFSNode(x=0, y=0, time=0, tool=Tool.Torch))

    while len(open_queue) > 0:

        space = heappop(open_queue)

        time = space.time
        x = space.x
        y = space.y
        tool = space.tool

        visited.add((x, y, tool))

        if x == target[0] and y == target[1] and tool == Tool.Torch:
            return time

        options = [(x, y), (x, y+1), (x-1, y), (x+1, y),  (x, y-1)]

        # add tools and time to the options
        options_with_tools = []
        for option in options:
            if (x == option[0]) and (y == option[1]):
                for option_tool in Tool:
                    options_with_tools.append(
                        (option[0], option[1], option_tool, time+7))
            else:
                options_with_tools.append((option[0], option[1], tool, time+1))

                # filter out invalid options
                compatible_options = []
                for option in options_with_tools:
                    if option[0] >= 0 and option[1] >= 0 and (option[0] < (target[0] + 300)) and (option[1] < (target[1] + 50)):
                        if (option[0], option[1], option[2]) not in visited:
                            terrain = get_terrain_type(
                                option[0], option[1], cave_depth, geologic_indexes, erosion_levels)
                            if is_terrain_compatible(terrain, option[2]) is True:
                                compatible_options.append(option)

        for compatible_option in compatible_options:
            queue_item = DFSNode(time=compatible_option[3],
                                 x=compatible_option[0],
                                 y=compatible_option[1],
                                 tool=compatible_option[2])

            if queue_item not in open_queue:
                heappush(open_queue, queue_item)



def main():
    risk_level = 0

    cave_depth = 11109
    target = (9, 731)
    # cave_depth = 510
    # target = (10, 10)

    # memoization of geologic indexes
    geologic_indexes = {}
    geologic_indexes[(0, 0)] = 0
    geologic_indexes[target] = 0

    # memoization of erosion levels
    erosion_levels = {}

    # pre-cache geologic indexes. They have to be built across X and then down Y
    # since their calculation depends on values calculated already for spots up
    # and to the left
    for y in range(target[1]+1000):
        for x in range(target[0]+1000):
            get_geologic_index(x, y, cave_depth, geologic_indexes, erosion_levels)

    # sum up th risk level for the rectangle including the entrance at 0,0, and
    # the target
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            terrain_type = get_terrain_type(x,y, cave_depth, geologic_indexes, erosion_levels)
            if terrain_type == TerrainType.WET:
                risk_level += 1
            elif terrain_type == TerrainType.NARROW:
                risk_level += 2

    print(f'Part 1: Risk level is: {risk_level}')

    min_time = get_minimum_time_bfs(target, cave_depth, geologic_indexes, erosion_levels)
    print(f'Part 2: Minimum time to reach target is: {min_time}')


if __name__ == "__main__":
    main()
