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
expansion_scale = 1


def expand_universe():
    galaxy_rows = {}
    for galaxy in galaxy_list:
        galaxy_rows[galaxy[1]] = True

    offset = 0
    row_num = 0
    while True:
        if row_num >= len(universe_map):
            break
        if not galaxy_rows.get(row_num-offset, False):
            for _ in range(0, expansion_scale):
                universe_map.insert(row_num, '.' * len(universe_map[0]))
                offset += 1
                row_num += 1

        row_num += 1

    galaxy_cols = {}
    for galaxy in galaxy_list:
        galaxy_cols[galaxy[0]] = True

    offset = 0
    col_num = 0
    while True:
        if col_num >= len(universe_map[0]):
            break
        if not galaxy_cols.get(col_num - offset, False):
            for row_num in range(0, len(universe_map)):
                new_str = '.' * expansion_scale
                universe_map[row_num] = universe_map[row_num][:col_num] + new_str + universe_map[row_num][col_num:]
            offset += 1 * expansion_scale
            col_num += 1 * expansion_scale

        col_num += 1

    # Recalculate galaxy locations after expansion
    galaxy_list.clear()
    for y in range(0, len(universe_map)):
        for x, char in enumerate(universe_map[y]):
            if char == '#':
                galaxy_list.append((x, y))


def get_shortest_distance(point1, point2):
    x_diff = abs(point1[0] - point2[0])
    y_diff = abs(point1[1] - point2[1])
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

    print("Universe mapped, expanding now...")
    expand_universe()
    print("Universe expanded, calculating distances...")

    score = 0

    # for row in universe_map:
    #     print(row)
    # print(galaxy_list)

    for index1, galaxy in enumerate(galaxy_list):
        for index2 in range(index1+1, len(galaxy_list)):
            score += get_shortest_distance(galaxy_list[index1], galaxy_list[index2])
    return score


if __name__ == '__main__':
    expansion_scale = 1
    score = calculate_score(test=False)
    print(f'Score: {score}')
