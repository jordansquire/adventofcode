from util.util import timeit

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    points = []
    for line in file:
        pts = line.strip().split(',')
        x = int(pts[0])
        y = int(pts[1])
        points.append((x, y))

    # Iterate through all point pairs and find the largest rectangle that can be generated
    max_size = 0
    for i, pt1 in enumerate(points):
        for j in range(i + 1, len(points)):
            pt2 = points[j]
            size = abs(pt1[0] - pt2[0] + 1) * abs(pt1[1] - pt2[1] + 1)
            if size > max_size:
                max_size = size

    return max_size

@timeit
def calculate_score_pt2(test: bool) -> int:
    from shapely.geometry import Polygon
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    points = []
    for line in file:
        pts = line.strip().split(',')
        x = int(pts[0])
        y = int(pts[1])
        points.append((x, y))

    # Iterate through all point pairs and find the largest rectangle that can
    # be generated that also if within the larger polygon
    floor_space = Polygon(points)
    max_size = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pt1 = points[i]
            pt2 = points[j]
            min_x = min(pt1[0], pt2[0])
            min_y = min(pt1[1], pt2[1])
            max_x = max(pt1[0], pt2[0])
            max_y = max(pt1[1], pt2[1])
            poly = Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
            if poly.is_valid:
                if floor_space.contains(poly):
                    size = (abs(pt1[0] - pt2[0]) + 1) * (abs(pt1[1] - pt2[1]) + 1)
                    if size > max_size:
                        max_size = size

    return max_size


if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 50
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 24
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')