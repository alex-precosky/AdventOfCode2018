"""Advent of Code 2018: Day 5"""
from string import ascii_lowercase


def check_if_should_eliminate(ch1, ch2):
    """Checks if characters ch1 and ch2 are the same letter but of opposite case"""
    if (ord(ch1) + 32 == ord(ch2)) or (ord(ch1) - 32) == ord(ch2):
        return True
    else:
        return False

def do_reduce(polymer_str):
    """Iterate through the polymer string, and zap pairs of characters that need zapping"""
    i = len(polymer_str) - 1

    while i > 0:
        if check_if_should_eliminate(polymer_str[i], polymer_str[i-1]) is True:
            polymer_str = polymer_str[0:i-1] + polymer_str[i+1:]
            i -= 2
        else:
            i -= 1

    return polymer_str

def do_reduce_loop(polymer_str):
    """Take a polymer string and keep calling do_reduce() on it until that doesn't make it any shorter"""
    current_str = polymer_str
    old_len = len(current_str)
    new_len = -1

    while old_len != new_len:
        old_len = len(current_str)
        current_str = do_reduce(current_str)
        new_len = len(current_str)

    return current_str


def main():
    input_str = open('input/Day5.txt').readline().strip()
    print(f'Initial length: {len(input_str)}')

    # Part 1 - what is the length of the polymer after fully reacting it?
    reduced_str = do_reduce_loop(input_str)
    print(f'Polymer length after fully reacting: {len(reduced_str)}')

    # Part 2 - remove all of one letter of the alphabet at the time, and fully react the polymer.
    # What is the shortest polymer we can produce this way? 
    shortest_polymer = len(input_str)

    for c in ascii_lowercase:
        input_str_minus_letter = list(filter(lambda x: x.lower() != c, input_str))
        reduced_str = do_reduce_loop(input_str_minus_letter)
        if len(reduced_str) < shortest_polymer:
            shortest_polymer = len(reduced_str)
            print(f'Shortest polymer so far: {shortest_polymer}')


if __name__ == "__main__":
    main()
