from util.util import timeit

test_data = [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3',
]
hail_storm = []


def generate_line(data):
    return (
        (data[0][0], data[0][1], data[0][2]),
        (data[0][0] + data[1][0], data[0][1] + data[1][1], data[0][2] + data[1][2])
    )


def find_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def in_the_future(intersection, hail):
    if intersection[0] >= hail[0][0] and hail[1][0] < 0:
        return False
    if intersection[0] <= hail[0][0] and hail[1][0] > 0:
        return False
    if intersection[1] >= hail[0][1] and hail[1][1] < 0:
        return False
    if intersection[1] <= hail[0][1] and hail[1][1] > 0:
        return False
    return True


@timeit
def calculate_score(test: bool, bounds) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        line_split = line.split('@')
        x, y, z = line_split[0].strip().split(',')
        dx, dy, dz = line_split[1].strip().split(',')
        hail_storm.append(((int(x), int(y), int(z)), (int(dx), int(dy), int(dz))))

    if not test:
        file.close()

    score = 0
    for i in range(len(hail_storm)):
        for j in range(i+1, len(hail_storm)):
            line1 = generate_line(hail_storm[i])
            line2 = generate_line(hail_storm[j])
            intersection = find_intersection(line1, line2)
            if intersection:
                if bounds[0] <= intersection[0] <= bounds[1] and bounds[0] <= intersection[1] <= bounds[1]:
                    if in_the_future(intersection, hail_storm[i]) and in_the_future(intersection, hail_storm[j]):
                        # print(f'Inbounds: {intersection}')
                        score += 1
                        continue

    return score


if __name__ == '__main__':
    # score = calculate_score(test=True, bounds=(7, 27))
    score = calculate_score(test=False, bounds=(200000000000000, 400000000000000))
    print(f'Score: {score}')
