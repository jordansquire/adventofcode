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
    next_x = location[0] + direction[0]
    next_y = location[1] + direction[1]
    super_x = location[2]
    super_y = location[3]

    if next_x < 0:
        next_x = len(garden_map[0]) - 1
        super_x -= 1

    if next_x >= len(garden_map[0]):
        next_x = 0
        super_x += 1

    if next_y < 0:
        next_y = len(garden_map) - 1
        super_y -= 1

    if next_y >= len(garden_map):
        next_y = 0
        super_y += 1

    next_location = (next_x, next_y, super_x, super_y)
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


@timeit
def calculate_score(test: bool, steps) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    start_location = (0, 0, 0, 0)  # (x, y, super_x, super_y)
    for y, line in enumerate(file):
        garden_map.append(line.strip())
        try:
            start_location = (line.index('S'), y, 0, 0)
        except ValueError:
            pass

    if not test:
        file.close()

    locations = set()
    locations.add(start_location)
    for step in range(steps):
        locations = find_steps(locations)
        # print(f'{step}: {len(locations)}')
        print(f'{len(locations)}')

    # print(locations)
    # print_garden(locations)
    return len(locations)


if __name__ == '__main__':
    score = calculate_score(test=True, steps=500)
    print(f'Score: {score}')
