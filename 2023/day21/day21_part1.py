from functools import cache
from util.util import timeit

test_data = [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........',
]
garden_map = []
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def valid_position(pos):
    return 0 <= pos[0] < len(garden_map[0]) and 0 <= pos[1] < len(garden_map)


@cache
def take_step(location, direction):
    next_location = (location[0] + direction[0], location[1] + direction[1])
    if valid_position(next_location):
        if garden_map[next_location[1]][next_location[0]] in '.S':
            return next_location


def find_steps(locations):
    possible_locations = set()
    for location in locations:
        for direction in DIRECTIONS:
            new_location = take_step(location, direction)
            if new_location:
                possible_locations.add(new_location)

    return possible_locations


def print_garden(locations):
    for y in range(len(garden_map)):
        line = ''
        for x in range(len(garden_map[0])):
            if (x, y) in locations:
                line += 'O'
            else:
                line += garden_map[y][x]
        print(line)


@timeit
def calculate_score(test: bool, steps) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    start_location = (0, 0)
    for y, line in enumerate(file):
        garden_map.append(line.strip())
        try:
            start_location = (line.index('S'), y)
        except ValueError:
            pass

    if not test:
        file.close()

    locations = set()
    locations.add(start_location)
    for _ in range(steps):
        locations = find_steps(locations)

    # print(locations)
    # print_garden(locations)
    return len(locations)


if __name__ == '__main__':
    score = calculate_score(test=False, steps=64)
    print(f'Score: {score}')
