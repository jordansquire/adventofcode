from functools import cache
from util.util import timeit

test_data = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....',
]
cache_map = {}


def tilt_map(rock_map, direction):
    if direction in ('north', 'south'):
        rock_map = [''.join(s) for s in zip(*rock_map)]

    for index, row in enumerate(rock_map):
        row = tilt_row(str(row), direction)
        rock_map[index] = row

    if direction in ('north', 'south'):
        rock_map = [''.join(s) for s in zip(*rock_map)]
    return rock_map


@cache
def tilt_row(row, direction):
    new_row = ''
    rock_count = 0
    blank_count = 0

    if direction in ('north', 'west'):
        row = row[::-1]

    for index, char in enumerate(row):
        if char == 'O':
            rock_count += 1
        if char == '.':
            blank_count += 1
        if char == '#':
            new_row = new_row + '.' * blank_count + 'O' * rock_count + '#'
            rock_count = blank_count = 0

    new_row = new_row + '.' * blank_count + 'O' * rock_count

    if direction in ('north', 'west'):
        new_row = new_row[::-1]

    return new_row


def hash_rocks(rock_map, direction):
    x = tuple(direction)
    for row in rock_map:
        w = [pos for pos, char in enumerate(row) if char == 'O']
        x += tuple(w)
    return hash(x)


def get_score(rock_map):
    score = 0
    for index, row in enumerate(rock_map):
        score += row.count('O') * (len(rock_map) - index)
    return score


@timeit
def calculate_score(test: bool, cycles=1) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    rock_map = []
    for line in file:
        line = line.strip()
        rock_map.append(line)

    if not test:
        file.close()

    repetition_start = None
    repetition_pace = []
    scores = []
    pace_found = False

    directions = ["north", "west", "south", "east"]
    for c in range(0, cycles):
        if pace_found:
            break
        for direction in directions:
            rhash = hash_rocks(rock_map, direction)
            if rhash in cache_map:
                rock_map = cache_map[rhash]
                if repetition_start is None:
                    repetition_start = {'hash': rhash, 'cycle': c}
                    repetition_pace.append(c)
                else:
                    if repetition_start['hash'] == rhash:
                        repetition_pace.append(c)

                        if len(repetition_pace) > 3 and \
                                repetition_pace[-1] - repetition_pace[-2] == repetition_pace[-2] - repetition_pace[-3]:
                            pace_found = True
                            print(f'Pace found: {repetition_pace[-1] - repetition_pace[-2]}')
                            break
            else:
                rock_map = tilt_map(rock_map, direction)
                cache_map[rhash] = rock_map

        scores.append(get_score(rock_map))

    max_cycle = repetition_pace[-2] + 1
    pace = repetition_pace[-1] - repetition_pace[-2]
    target_cycle = cycles % pace
    score = scores[max_cycle + pace - target_cycle + 1]

    return score


if __name__ == '__main__':
    score = calculate_score(test=False, cycles=1_000_000_000)
    print(f'Score: {score}')
