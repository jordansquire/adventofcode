from functools import cache
from util.util import timeit

test_data = [
    '..@@.@@@@.',
    '@@@.@.@.@@',
    '@@@@@.@.@@',
    '@.@@@@..@.',
    '@@.@@@@.@@',
    '.@@@@@@@.@',
    '.@.@.@.@@@',
    '@.@@@.@@@@',
    '.@@@@@@@@.',
    '@.@.@@@.@.',
]

map = []
DIRECTIONS = [(-1,-1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def populate_map(test: bool):
    map.clear()
    check_position.cache_clear()
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        row = []
        for x, char in enumerate(line.strip()):
            row.append(char)
        map.append(row)


def valid_position(pos):
    """
    Check if the given position is within the map
    """
    return 0 <= pos[0] < len(map[0]) and 0 <= pos[1] < len(map)


@cache
def check_position(pos):
    """
    Check if a given position is occupied
    """
    if valid_position(pos):
        if map[pos[1]][pos[0]] == '@':
            return 1
    return 0


def remove_rolls(rolls_to_remove):
    """
    Removes a list of rolls from the map by position
    """
    for roll in rolls_to_remove:
        map[roll[1]][roll[0]] = '.'


@timeit
def calculate_score_pt1(test: bool) -> int:
    populate_map(test)

    score = 0
    for y, _ in enumerate(map):
        for x in range(len(map)):
            # Skip empty squares
            if map[y][x] != '@':
                continue

            neighbors = 0
            for direction in DIRECTIONS:
                # Check each neighboring square
                neighbor = (x + direction[0], y + direction[1])
                neighbors += check_position(neighbor)

            if neighbors < 4:
                score += 1
                # print('(', x, ',', y, ')', neighbors, map[y][x])
    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    populate_map(test)

    score = 0
    while True:
        rolls_to_remove = []
        for y, _ in enumerate(map):
            for x in range(len(map)):
                # Skip empty squares
                if map[y][x] != '@':
                    continue

                neighbors = 0
                for direction in DIRECTIONS:
                    # Check each neighboring square
                    neighbor = (x + direction[0], y + direction[1])
                    neighbors += check_position(neighbor)

                if neighbors < 4:
                    score += 1
                    rolls_to_remove.append((x, y))

        if len(rolls_to_remove) == 0:
            return score
        else:
            remove_rolls(rolls_to_remove)
            check_position.cache_clear()



if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 13
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 43
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')