"""Advent of Code 2018: Day 2"""
def build_dict(boxID):
    return_dict = {}

    for letter in boxID:
        if letter not in return_dict:
            return_dict[letter] = 1
        else:
            return_dict[letter] += 1

    return return_dict

def check_repeat_n(boxID_dict, n):
    for letter in boxID_dict.keys():
        if boxID_dict[letter] == n:
            return True

    return False

def remove_letter_n(boxID, n):
    return boxID[0:n] + boxID[n+1:]

def find_checksum(boxIDs):
    twoCount = 0
    threeCount = 0
    for boxID in boxIDs:

        letterDict = build_dict(boxID)

        if check_repeat_n(letterDict, 2) is True:
            twoCount += 1

        if check_repeat_n(letterDict, 3) is True:
            threeCount += 1
    
    checksum = twoCount * threeCount

    return checksum

def find_common_part_of_target_box(boxIDs):
    id_len = len(boxIDs[0])

    for i in range(id_len):
        id_set = set()
        for boxID in boxIDs:
            box_id_missing_letter = remove_letter_n(boxID, i)
            if box_id_missing_letter in id_set:
                return box_id_missing_letter
            else:
                id_set.add(box_id_missing_letter)

    return 'Not found'


if __name__ == "__main__":

    boxIDs = [line.strip() for line in open("input/Day2.txt").readlines()]

    checksum = find_checksum(boxIDs)
    print(f'The checksum is {checksum}')

    target_box_id_common_part = find_common_part_of_target_box(boxIDs)
    print(f'The common part of the target boxes is {target_box_id_common_part}')
