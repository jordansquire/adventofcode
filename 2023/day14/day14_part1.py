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


def tilt_row(row):
    new_row = ''
    rock_count = 0
    blank_count = 0
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

    return new_row[::-1]


@timeit
def calculate_score(test: bool) -> int:
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

    score = 0
    rock_map = [''.join(s) for s in zip(*rock_map)]

    for index, row in enumerate(rock_map):
        row = tilt_row(row)
        rock_map[index] = row

    rock_map = [''.join(s) for s in zip(*rock_map)]
    for index, row in enumerate(rock_map):
        score += row.count('O') * (len(rock_map) - index)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
