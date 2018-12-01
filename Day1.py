if __name__ == "__main__":
    frequency = 0
    frequency_dict = {}
    repeat_seen = False

    changes = []
    for line in open("input/Day1.txt").readlines():
        if frequency in frequency_dict and not repeat_seen:
            print(f'Frequency {frequency} was seen twice first')
            repeat_seen = True
        else:
            frequency_dict[frequency] = 1

        change = int(line)
        frequency += change
        changes.append(change)

    print(frequency)

    # Part 2: Keep applying frequency changes from the input list until a frequency is seen twice
    i = 0
    while not repeat_seen:
        if frequency in frequency_dict and not repeat_seen:
            print(f'Frequency {frequency} was seen twice first')
            repeat_seen = True
        else:
            frequency_dict[frequency] = 1

        change = changes[i]
        frequency += change
        i = (i+1) % len(changes)
