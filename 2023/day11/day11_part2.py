from util.util import timeit

test_data = [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....',
]
universe_map = []
galaxy_list = []
warp_rows = []
warp_cols = []
expansion_scale = 1


def expand_universe():
    galaxy_rows = {}
    for galaxy in galaxy_list:
        galaxy_rows[galaxy[1]] = True

    for y in range(0, len(universe_map)):
        if not galaxy_rows.get(y, False):
            warp_rows.append(y)

    galaxy_cols = {}
    for galaxy in galaxy_list:
        galaxy_cols[galaxy[0]] = True

    for x in range(0, len(universe_map[0])):
        if not galaxy_cols.get(x, False):
            warp_cols.append(x)


def get_shortest_distance(point1, point2):
    x_diff = abs(point1[0] - point2[0])
    for col in warp_cols:
        if point1[0] < col < point2[0] or point2[0] < col < point1[0]:
            x_diff += expansion_scale-1

    y_diff = abs(point1[1] - point2[1])
    for row in warp_rows:
        if point1[1] < row < point2[1] or point2[1] < row < point1[1]:
            y_diff += expansion_scale-1
    distance = x_diff + y_diff

    # print(f'Pt1: {point1}, Pt2: {point2}, x_diff: {x_diff}, y:diff {y_diff}, distance {distance}')
    return distance


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        universe_map.append(line.strip())
        for x, char in enumerate(line):
            if char == '#':
                galaxy_list.append((x, y))

    if not test:
        file.close()

    expand_universe()
    score = 0

    # for row in universe_map:
    #     print(row)
    # print(galaxy_list)

    for index1, galaxy in enumerate(galaxy_list):
        for index2 in range(index1+1, len(galaxy_list)):
            score += get_shortest_distance(galaxy_list[index1], galaxy_list[index2])
    return score


if __name__ == '__main__':
    expansion_scale = 1_000_000
    score = calculate_score(test=False)
    print(f'Score: {score}')