from util.util import timeit
from functools import cache

@cache
def _stone_rules(stone: int):
    # Apply rules
    if stone == 0:
        return [1, None]

    num_len = len(str(stone))
    if not num_len % 2:
        return [int(str(stone)[0:int(num_len/2)]), int(str(stone)[int(num_len/2):])]

    return [stone * 2024, None]

@cache
def _count_recursive(stone, blink):
    left_stone, right_stone = _stone_rules(stone)

    if blink == 1:
        # We reached the end
        if right_stone is None:
            return 1
        else:
            return 2

    score = _count_recursive(left_stone, blink - 1)
    if right_stone is not None:
        score += _count_recursive(right_stone, blink - 1)

    return score

@timeit
def calculate_score_pt1(test: bool, blinks: int = 25) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    stones = [int(x) for x in file.readline().split()]
    for n in range(blinks):
        new_stones = []
        for stone in stones:
            for s in _stone_rules(stone):
                if s is not None:
                    new_stones.append(s)
        stones = new_stones

    return len(stones)


@timeit
def calculate_score_pt2(test: bool, blinks: int = 75) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    stones = [int(x) for x in file.readline().split()]
    score = 0
    for stone in stones:
        # Recursively count the path of each stone
        score += _count_recursive(stone, blinks)

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False, blinks=25)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False, blinks=75)
    print(f'Score: {score}')
