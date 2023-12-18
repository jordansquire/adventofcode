from shapely.geometry.polygon import Polygon
from util.util import timeit

test_data = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]
path = []


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    cursor = (0, 0)
    x_delta = 0
    y_delta = 0
    direction = ''
    for row_num, line in enumerate(file):
        line_split = line.strip().split()
        hex_code = line_split[2][2:-1]
        direction_code = hex_code[-1]
        spaces_hex = hex_code[0:-1]

        if direction_code == '0':
            direction = 'R'
        if direction_code == '1':
            direction = 'D'
        if direction_code == '2':
            direction = 'L'
        if direction_code == '3':
            direction = 'U'

        spaces = int(spaces_hex, 16)

        if direction == 'R':
            x_delta += spaces
            path.append((cursor[0] + spaces, cursor[1]))
        if direction == 'L':
            x_delta += spaces
            path.append((cursor[0] - spaces, cursor[1]))
        if direction == 'D':
            y_delta += spaces
            path.append((cursor[0], cursor[1] + spaces))
        if direction == 'U':
            y_delta += spaces
            path.append((cursor[0], cursor[1] - spaces))
        cursor = path[-1]

    if not test:
        file.close()

    polygon = Polygon(path)
    # print(f'Area: {polygon.area} {polygon.area + y_delta/2 + x_delta/2 + 1}')

    return int(polygon.area + y_delta/2 + x_delta/2 + 1)


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
