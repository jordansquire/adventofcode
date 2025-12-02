import math
from enum import Enum
from functools import cache

from util.util import timeit

class Operations(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

a = 0
b = 0
c = 0
instr_ptr = 0
output = ''

def _get_combo(val: int) -> int:
    if val <= 3:
        return val
    if val == 4:
        return a
    if val == 5:
        return b
    return c

def _execute(cmd: Operations, operand: int):
    global a, b, c, instr_ptr, output
    if cmd == Operations.ADV:
        a = math.floor(a / (2**_get_combo(operand)))
    if cmd == Operations.BXL:
        b = b ^ operand
    if cmd == Operations.BST:
        b = _get_combo(operand) % 8
    if cmd == Operations.JNZ:
        if a != 0:
            instr_ptr = operand
            return
    if cmd == Operations.BXC:
        b = b ^ c
    if cmd == Operations.OUT:
        output += str(_get_combo(operand) % 8) + ','
    if cmd == Operations.BDV:
        b = math.floor(a / (2 ** _get_combo(operand)))
    if cmd == Operations.CDV:
        c = math.floor(a / (2 ** _get_combo(operand)))

    instr_ptr += 2

@timeit
def calculate_score_pt1(test: bool):
    if test:
        file = open("test2.txt", "r")
    else:
        file = open("input.txt", "r")

    global a, b, c, instr_ptr
    program = []
    for line in file:
        l = line.strip().split(':')
        if l[0] == 'Register A':
            a = int(l[1])
        if l[0] == 'Register B':
            b = int(l[1])
        if l[0] == 'Register C':
            c = int(l[1])
        if l[0] == 'Program':
            program = [int(x) for x in l[1].split(',')]

    # print(a, b, c, program)
    while instr_ptr < len(program):
        _execute(Operations(program[instr_ptr]), program[instr_ptr+1])
    print(output[:-1])

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test2.txt", "r")
    else:
        file = open("input.txt", "r")

    global a, b, c, instr_ptr, output
    program = []
    program_str = ''
    orig_b = orig_c = 0
    for line in file:
        l = line.strip().split(':')
        # if l[0] == 'Register A':
        #     a = int(l[1])
        if l[0] == 'Register B':
            orig_b = int(l[1])
        if l[0] == 'Register C':
            orig_c = int(l[1])
        if l[0] == 'Program':
            program_str = l[1].strip()
            program = [int(x) for x in l[1].split(',')]

    trial_a = 35184372088832
    while True:
        a = trial_a
        b = orig_b
        c = orig_c
        instr_ptr = 0
        output = ''
        while instr_ptr < len(program):
            _execute(Operations(program[instr_ptr]), program[instr_ptr + 1])
            if output != '' and  output[:-1] != program_str[0:len(output)-1]:
                break

        if output[:-1] == program_str:
            print(output[:-1])
            return trial_a

        trial_a += 2097152

        if trial_a % 10_000 == 0:
            print(trial_a)

        # if len(output[:-1]) == len(program_str):
        #     return trial_a
        # else:
        #     print(len(output), len(program_str), trial_a)
        #     trial_a *= 2

        if len(output[:-1]) > len(program_str):
            return 0


if __name__ == '__main__':
    calculate_score_pt1(test=True)

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')