def apply_change_check_duplicate(frequency, change, frequency_dict):

    is_repeat = False

    if frequency in frequency_dict:
        is_repeat = True
    else:
        frequency_dict[frequency] = 1

    frequency += change

    return frequency, is_repeat

if __name__ == "__main__":
    frequency = 0
    frequency_dict = {}
    repeat_seen = False

    changes = []
    for line in open("input/Day1.txt").readlines():
        change = int(line)
        frequency, is_repeat = apply_change_check_duplicate(frequency, change, frequency_dict)

        if is_repeat and not repeat_seen:
            repeat_seen = True
            print(f'Frequency {frequency} was seen twice')

        changes.append(change)

    print(frequency)

    # Part 2: Keep applying frequency changes from the input list until a frequency is seen twice
    i = 0
    while not repeat_seen:
        change = changes[i]
        frequency, is_repeat = apply_change_check_duplicate(frequency, change, frequency_dict)
        i = (i+1) % len(changes)

        if is_repeat:
            repeat_seen = True
            print(f'Frequency {frequency} was seen twice')
