import statistics
from util.util import timeit

def _extract_xy(text: str) -> (int, int):
    x = text.split('=')[1].split(',')[0]
    y = text.split('=')[1].split(',')[1]
    return int(x), int(y)

def _keep_within_bounds(val: int, boundary: int):
    if val > boundary:
        val = val - boundary - 1

    if val < 0:
        val = boundary + val + 1

    return val

def _move_point(pt: (int, int), vel: (int, int), bounds: (int, int)) -> (int, int):
    x = _keep_within_bounds(pt[0] + vel[0], bounds[0])
    y = _keep_within_bounds(pt[1] + vel[1], bounds[1])
    return x, y

def _print_map(vectors, bounds):
    points = set()
    for vector in vectors:
        points.add(vector['pt'])

    for y in range(bounds[1]):
        line = ''
        for x in range(bounds[0]):
            if (x,y) in points:
                line += 'X'
            else:
                line += '.'
        print(line)

def _calculate_deviation(vectors):
    points_x = []
    points_y = []
    for vector in vectors:
        points_x.append(vector['pt'][0])
        points_y.append(vector['pt'][1])

    return statistics.stdev(points_x) + statistics.stdev(points_y)

@timeit
def calculate_score_pt1(test: bool) -> int:
    bounds = (101-1, 103-1)
    if test:
        file = open("test.txt", "r")
        bounds = (11-1, 7-1)
    else:
        file = open("input.txt", "r")

    vectors = []
    for line in file:
        sp = line.split(' ')
        x, y = _extract_xy(sp[0])
        dx, dy = _extract_xy(sp[1])
        vectors.append({'pt': (x, y), 'vel': (dx, dy)})

    for seconds in range(100):
        for i, vector in enumerate(vectors):
            vectors[i]['pt'] = _move_point(vector['pt'], vector['vel'], bounds)

    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    mid_x = bounds[0] / 2
    mid_y = bounds[1] / 2
    for vector in vectors:
        if vector['pt'][0] < mid_x and vector['pt'][1] < mid_y:
            quadrants[1] += 1
        if vector['pt'][0] > mid_x and vector['pt'][1] < mid_y:
            quadrants[2] += 1
        if vector['pt'][0] < mid_x and vector['pt'][1] > mid_y:
            quadrants[3] += 1
        if vector['pt'][0] > mid_x and vector['pt'][1] > mid_y:
            quadrants[4] += 1

    print(quadrants)
    return quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]

@timeit
def calculate_score_pt2(test: bool) -> int:
    bounds = (101 - 1, 103 - 1)
    if test:
        file = open("test.txt", "r")
        bounds = (11 - 1, 7 - 1)
    else:
        file = open("input.txt", "r")

    vectors = []
    for line in file:
        sp = line.split(' ')
        x, y = _extract_xy(sp[0])
        dx, dy = _extract_xy(sp[1])
        vectors.append({'pt': (x, y), 'vel': (dx, dy)})

    min_dev = 100000
    min_dev_time = 0
    deviations = {}
    for seconds in range(10000):
        for i, vector in enumerate(vectors):
            vectors[i]['pt'] = _move_point(vector['pt'], vector['vel'], bounds)

        std_dev = _calculate_deviation(vectors)
        deviations[seconds] = std_dev
        if std_dev <= min_dev:
            min_dev = std_dev
            min_dev_time = seconds
            print(seconds)
            _print_map(vectors, bounds)
            print()

    return min_dev_time + 1

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
