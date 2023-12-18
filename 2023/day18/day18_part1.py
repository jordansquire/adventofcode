from shapely.geometry import Point
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
instructions = []
path = []


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    cursor = (0, 0)
    for row_num, line in enumerate(file):
        line_split = line.strip().split()
        direction = line_split[0]
        spaces = int(line_split[1])
        color = line_split[2][1:-1]
        instructions.append((direction, spaces, color))

        if direction == 'R':
            for x in range(spaces):
                path.append((cursor[0] + 1, cursor[1]))
                cursor = path[-1]
        if direction == 'L':
            for x in range(spaces):
                path.append((cursor[0] - 1, cursor[1]))
                cursor = path[-1]
        if direction == 'D':
            for y in range(spaces):
                path.append((cursor[0], cursor[1] + 1))
                cursor = path[-1]
        if direction == 'U':
            for y in range(spaces):
                path.append((cursor[0], cursor[1] - 1))
                cursor = path[-1]

    if not test:
        file.close()

    score = 0

    max_x = max(path, key=lambda item: item[0])[0]
    min_x = min(path, key=lambda item: item[0])[0]
    max_y = max(path, key=lambda item: item[1])[1]
    min_y = min(path, key=lambda item: item[1])[1]
    polygon = Polygon(path)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in path:
                score += 1
            else:
                point = Point(x, y)
                score += polygon.contains(point)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
