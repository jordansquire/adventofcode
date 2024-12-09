import itertools
from util.util import timeit

antenna_map = []

def _valid_point(pt: (int, int)):
    return (
        pt[0] < len(antenna_map) and
        pt[1] < len(antenna_map[0]) and
        pt[0] >= 0 and
        pt[1] >= 0
    )

def _get_slope(pt1: (int, int), pt2: (int, int)) -> (int, int):
    return pt1[0] - pt2[0],  pt1[1] - pt2[1]

def _get_next_point(pt: (int, int), slope: (int, int), right: bool = True) -> (int, int):
    if right:
        return pt[0] + slope[0], pt[1] + slope[1]
    else:
        return pt[0] - slope[0], pt[1] - slope[1]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    for line in file:
        antenna_map.append(list(line.strip()))


    unique_chars = set()
    for line in antenna_map:
        unique_chars = unique_chars.union(set(line))

    unique_chars.remove('.')

    anti_nodes = set()
    for char in unique_chars:
        points = []

        # Find all the locations of the character
        for y, row in enumerate(antenna_map):
            x_loc = [i for i, x in enumerate(row) if x == char]
            for x in x_loc:
                points.append((x,y))

        point_pairs = list(itertools.combinations(points, 2))
        # print(char, points)
        for pairs in point_pairs:
            slope = _get_slope(pairs[0], pairs[1])

            next_pt = _get_next_point(pairs[0], slope, right=True)
            if next_pt in pairs:
                next_pt = _get_next_point(next_pt, slope, right=True)
            if _valid_point(next_pt):
                anti_nodes.add(next_pt)

            next_pt = _get_next_point(pairs[0], slope, right=False)
            if next_pt in pairs:
                next_pt = _get_next_point(next_pt, slope, right=False)
            if _valid_point(next_pt):
                anti_nodes.add(next_pt)

    return len(anti_nodes)

@timeit
def calculate_score_pt2() -> int:
    unique_chars = set()
    for line in antenna_map:
        unique_chars = unique_chars.union(set(line))

    unique_chars.remove('.')

    anti_nodes = set()
    for char in unique_chars:
        points = []

        # Find all the locations of the character
        for y, row in enumerate(antenna_map):
            x_loc = [i for i, x in enumerate(row) if x == char]
            for x in x_loc:
                points.append((x, y))

        point_pairs = list(itertools.combinations(points, 2))

        for pairs in point_pairs:
            slope = _get_slope(pairs[0], pairs[1])
            anti_nodes.add(pairs[0])
            anti_nodes.add(pairs[1])

            # Check points to the right
            next_pt = _get_next_point(pairs[0], slope, right=True)
            while _valid_point(next_pt):
                # if next_pt not in pairs:
                anti_nodes.add(next_pt)
                next_pt = _get_next_point(next_pt, slope, right=True)

            # Check points to the left
            next_pt = _get_next_point(pairs[0], slope, right=False)
            while _valid_point(next_pt):
                # if next_pt not in pairs:
                anti_nodes.add(next_pt)
                next_pt = _get_next_point(next_pt, slope, right=False)

    return len(anti_nodes)

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2()
    print(f'Score: {score}')
