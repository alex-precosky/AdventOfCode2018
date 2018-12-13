"""Advent of Code 2018: Day 13"""
from enum import Enum, IntEnum, auto
import io
import numpy as np

class TrackType(IntEnum):
    EMPTY = 0
    FORWARD_SLASH = 1
    BACK_SLASH = 2
    VERTICAL = 3
    HORIZONTAL = 4
    INTERSECTION = 5

    @classmethod
    def from_char(self, char):
        if char == ' ':
            track_type = TrackType.EMPTY
        elif char == '/':
            track_type = TrackType.FORWARD_SLASH
        elif char == '\\':
            track_type = TrackType.BACK_SLASH
        elif char == '|' or char == 'v' or char == '^':
            track_type = TrackType.VERTICAL
        elif char == '-' or char == '<' or char == '>':
            track_type = TrackType.HORIZONTAL
        elif char == '+':
            track_type = TrackType.INTERSECTION
        else:
            print(f"Invalid track type: {char}")

        return track_type

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @classmethod
    def from_char(self, char):
        if char == '^':
            return Direction.UP
        elif char == 'v':
            return Direction.DOWN
        elif char == '<':
            return Direction.LEFT
        elif char == '>':
            return Direction.RIGHT
        else:
            print('Invalid direction')

class Turn(Enum):
    LEFT = auto()
    STRAIGHT = auto()
    RIGHT = auto()

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.last_turn = Turn.RIGHT

class Track:
    def __init__(self):
        self.carts = []
        self.width = 0
        self.height = 0
        self.track_array = None

    def is_cart(self, char):
        if char == 'v' or char == '^' or char == '<' or char == '>':
            return True
        else:
            return False

    @classmethod
    def from_str(self, track_str):
        return_track = Track()

        buf = io.StringIO(track_str)
        height = 0
        for line in buf:
            width = len(line) - 1 # -1 because newline
            height += 1

        return_track.width = width
        return_track.height = height

        return_track.track_array = np.zeros([height, width])

        buf = io.StringIO(track_str)
        for row in range(height):
            line = buf.readline()
            for col in range(width):
                char = line[col]
                track_type = TrackType.from_char(char)
                return_track.track_array[row, col] = track_type
                if return_track.is_cart(char) is True:
                    direction = Direction.from_char(char)
                    return_track.carts.append(Cart(col, row, direction))

        return return_track

    def get_new_cart_direction(self, cart):
        track_type = self.track_array[cart.y, cart.x]
        direction = cart.direction

        if track_type == TrackType.VERTICAL or track_type == TrackType.HORIZONTAL:
            new_direction = direction

        elif track_type == TrackType.FORWARD_SLASH:
            if direction == Direction.UP:
                new_direction = Direction.RIGHT
            elif direction == Direction.DOWN:
                new_direction = Direction.LEFT
            elif direction == Direction.LEFT:
                new_direction = Direction.DOWN
            elif direction == Direction.RIGHT:
                new_direction = Direction.UP

        elif track_type == TrackType.BACK_SLASH:
            if direction == Direction.UP:
                new_direction = Direction.LEFT
            elif direction == Direction.DOWN:
                new_direction = Direction.RIGHT
            elif direction == Direction.LEFT:
                new_direction = Direction.UP
            elif direction == Direction.RIGHT:
                new_direction = Direction.DOWN

        elif track_type == TrackType.INTERSECTION:
            if cart.last_turn == Turn.LEFT:
                this_turn = Turn.STRAIGHT
            elif cart.last_turn == Turn.STRAIGHT:
                this_turn = Turn.RIGHT
            elif cart.last_turn == Turn.RIGHT:
                this_turn = Turn.LEFT

            if direction == Direction.UP:
                if this_turn == Turn.LEFT:
                    new_direction = Direction.LEFT
                elif this_turn == Turn.RIGHT:
                    new_direction = Direction.RIGHT
                else:
                    new_direction = direction

            elif direction == Direction.DOWN:
                if this_turn == Turn.LEFT:
                    new_direction = Direction.RIGHT
                elif this_turn == Turn.RIGHT:
                    new_direction = Direction.LEFT
                else:
                    new_direction = direction

            elif direction == Direction.LEFT:
                if this_turn == Turn.LEFT:
                    new_direction = Direction.DOWN
                elif this_turn == Turn.RIGHT:
                    new_direction = Direction.UP
                else:
                    new_direction = direction

            elif direction == Direction.RIGHT:
                if this_turn == Turn.LEFT:
                    new_direction = Direction.UP
                elif this_turn == Turn.RIGHT:
                    new_direction = Direction.DOWN
                else:
                    new_direction = direction

            cart.last_turn = this_turn
        else:
            print(f'Invalid track type: {track_type}')

        return new_direction

    def check_collisions(self, remaining_carts):
        position_set = set()

        for cart in remaining_carts:
            position_set.add((cart.x, cart.y))

        if len(position_set) < len(remaining_carts):
            return True
        else:
            return False

    def update_carts(self):

        crashed_carts = []
        remaining_carts = self.carts.copy()

        crash_location = None

        for cart in self.carts:
            if cart in crashed_carts:
                continue

            if cart.direction == Direction.UP:
                cart.y -= 1
            elif cart.direction == Direction.DOWN:
                cart.y += 1
            elif cart.direction == Direction.LEFT:
                cart.x -= 1
            elif cart.direction == Direction.RIGHT:
                cart.x += 1
            else:
                print('Invalid cart direction')

            cart.direction = self.get_new_cart_direction(cart)
            
            if self.check_collisions(remaining_carts) is True:

                # find all carts at this location
                remaining_carts.remove(cart)
                crashed_carts.append(cart)
                for cart2 in self.carts:
                    if (cart2.x == cart.x) and (cart2.y == cart.y) and (cart2 is not cart):
                        remaining_carts.remove(cart2)
                        crashed_carts.append(cart2)

                crash_location = cart.x, cart.y

        self.carts = remaining_carts

        return crash_location

def main():
    track = Track.from_str(open('input/day13.txt').read())

    collision_location = None
    steps = 0
    while collision_location is None:
        collision_location = track.update_carts()
        steps += 1

    print(f'First collision at {collision_location[0]},{collision_location[1]} at time {steps}')

    while len(track.carts) != 1:
        collision_location = track.update_carts()
        steps += 1

    last_cart = track.carts[0]
    print(f'Last cart at {last_cart.x},{last_cart.y} at time {steps}')

if __name__ == "__main__":
    main()
