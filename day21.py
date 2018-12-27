"""Advent of Code 2018: Day 21"""
import re
import copy


class Operation:
    def __init__(self, opcode, srcA, srcB, dest):
        self.opcode = opcode
        self.srcA = srcA
        self.srcB = srcB
        self.dest = dest


def execute_operation(operation, registers, ip_reg):

    if operation.opcode == 'addr':
        registers[operation.dest] = registers[operation.srcA] + registers[operation.srcB]

    elif operation.opcode == 'addi':
        registers[operation.dest] = registers[operation.srcA] + operation.srcB

    elif operation.opcode == 'mulr':
        registers[operation.dest] = registers[operation.srcA] * registers[operation.srcB]

    elif operation.opcode == 'muli':
        registers[operation.dest] = registers[operation.srcA] * operation.srcB

    elif operation.opcode == 'banr':
        registers[operation.dest] = registers[operation.srcA] & registers[operation.srcB]

    elif operation.opcode == 'bani':
        registers[operation.dest] = registers[operation.srcA] & operation.srcB

    elif operation.opcode == 'borr':
        registers[operation.dest] = registers[operation.srcA] | registers[operation.srcB]

    elif operation.opcode == 'bori':
        registers[operation.dest] = registers[operation.srcA] | operation.srcB

    elif operation.opcode == 'setr':
        registers[operation.dest] = registers[operation.srcA]

    elif operation.opcode == 'seti':
        registers[operation.dest] = operation.srcA

    elif operation.opcode == 'gtir':
        if operation.srcA > registers[operation.srcB]:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    elif operation.opcode == 'gtri':
        if registers[operation.srcA] > operation.srcB:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    elif operation.opcode == 'gtrr':
        if registers[operation.srcA] > registers[operation.srcB]:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    elif operation.opcode == 'eqir':
        if operation.srcA == registers[operation.srcB]:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    elif operation.opcode == 'eqri':
        if registers[operation.srcA] == operation.srcB:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    elif operation.opcode == 'eqrr':
        if registers[operation.srcA] == registers[operation.srcB]:
            registers[operation.dest] = 1
        else:
            registers[operation.dest] = 0

    else:
        print('Invalid instruction')


def main():
    # By examining the elf code, we see that the program halts when register F
    # (5) equals register A. And register A isn't touched elsewhere in the
    # program

    # So, Part 1 solution is to just find the value of register F when the
    # comparison is made that can halt the program

    # Part 2 looks for the last value of register F before the register F values
    # repeat

    in_file = open('input/Day21.txt')

    # First line specifies which regiter is the program counter
    ip_line = in_file.readline().strip()
    ip_reg = int(re.search(r'\d+', ip_line).group(0))

    operations = []
    for line in in_file.readlines():
        components = line.strip().split(' ')
        opcode = components[0]
        srcA = int(components[1])
        srcB = int(components[2])
        dest = int(components[3])

        operations.append(Operation(opcode, srcA, srcB, dest))

    ip = 0

    registers = [0, 0, 0, 0, 0, 0]

    f_set = set()
    lastF = 0
    regF = 0

    while True:
        registers[ip_reg] = ip
        execute_operation(operations[ip], registers, ip_reg)

        if operations[ip].opcode == 'eqrr':
            regF = registers[5]

            if len(f_set) == 0:
                print(f'Part 1: {regF}')

            if regF in f_set:
                print(f"Part 2: {lastF}")
                break
            f_set.add(regF)
            lastF = regF

        ip = registers[ip_reg]
        ip += 1

        if ip > len(operations)-1:
            print(f'program halted')
            break


if __name__ == "__main__":
    main()
