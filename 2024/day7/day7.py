import itertools

from enum import Enum
from util.util import timeit

class Operations(Enum):
    PLUS = 1
    MULT = 2
    CONCAT = 3

def _evaluate(numbers: list, operations: list) -> int:
    total = numbers[0]
    for i, operation in enumerate(operations):
        if operation == Operations.PLUS:
            total += numbers[i + 1]
        elif operation == Operations.MULT:
            total *= numbers[i + 1]
        elif operation == Operations.CONCAT:
            total = int(str(total) + str(numbers[i + 1]))
    return total

def _rotate_operations(operations: list) -> list:
    for i, operation in enumerate(operations):
        if operation == Operations.PLUS:
            operations[i] = Operations.MULT
            return operations
        elif operation == Operations.MULT:
            operations[i] = Operations.PLUS

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        x = line.split(':')
        total = int(x[0])
        numbers = x[1].split()
        numbers = [int(number) for number in numbers]

        operations = []
        for _ in range(len(numbers) - 1):
            operations.append(Operations.PLUS)

        while True:
            val = _evaluate(numbers, operations)
            if val == total:
                score += val
                break

            if Operations.PLUS not in operations:
                break

            operations = _rotate_operations(operations)

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    all_operations = [Operations.PLUS, Operations.MULT, Operations.CONCAT]

    score = 0
    for line in file:
        x = line.split(':')
        total = int(x[0])
        numbers = x[1].split()
        numbers = [int(number) for number in numbers]

        operation_slots = []
        for _ in range(len(numbers) - 1):
            operation_slots.append(all_operations)

        operation_possibilities = list(itertools.product(*operation_slots))

        for operations in operation_possibilities:
            val = _evaluate(numbers, operations)
            if val == total:
                score += val
                break

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
