from shapely.geometry.polygon import Polygon
from shapely.affinity import translate
import matplotlib.pyplot as plt
import geopandas as gpd
from util.util import timeit

test_data = [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9',
]
# test_data = [
#     '2,2,2~2,2,2',
# ]
bricks = []
SCALE = 0.95


def size(brick, axis):
    a = 0
    if axis == 'y':
        a = 1
    if axis == 'z':
        a = 2

    return abs(brick[a][1] - brick[a][0])


def get_min(brick1, brick2, n):
    return min(int(brick1[n]), int(brick2[n]))


def get_max(brick1, brick2, n):
    return max(int(brick1[n]), int(brick2[n]))


def move_brick(x_bricks, y_bricks, i):
    while True:
        if x_bricks[i].bounds[1] > 1:  # Above the ground
            x_bricks[i] = translate(x_bricks[i], 0, -1)
            y_bricks[i] = translate(y_bricks[i], 0, -1)
        else:
            return

        for j in range(len(x_bricks)):
            if j == i:
                continue
            if x_bricks[i].bounds[1] <= x_bricks[j].bounds[1] >= x_bricks[i].bounds[3]:
                if x_bricks[i].intersects(x_bricks[j]) and y_bricks[i].intersects(y_bricks[j]):
                    # Undo translate
                    x_bricks[i] = translate(x_bricks[i], 0, 1)
                    y_bricks[i] = translate(y_bricks[i], 0, 1)

                    # print_bricks(x_bricks)
                    # print_bricks(y_bricks)
                    return


def move_down(x_bricks, y_bricks):
    for i in range(len(x_bricks)):
        move_brick(x_bricks, y_bricks, i)


def print_bricks(b):
    p = gpd.GeoSeries(b)
    p.plot()
    plt.show()


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    x_bricks = []
    y_bricks = []
    for line in file:
        line_split = line.split('~')
        brick_start = line_split[0].split(',')
        brick_end = line_split[1].split(',')
        # (0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)
        min_x = get_min(brick_start, brick_end, 0)
        max_x = get_max(brick_start, brick_end, 0)
        min_y = get_min(brick_start, brick_end, 1)
        max_y = get_max(brick_start, brick_end, 1)
        min_z = get_min(brick_start, brick_end, 2)
        max_z = get_max(brick_start, brick_end, 2)

        x_path = [(min_x, min_z), (max_x + SCALE, min_z), (max_x + SCALE, max_z + SCALE), (min_x, max_z + SCALE)]
        x_bricks.append(Polygon(x_path))
        y_path = [(min_y, min_z), (max_y + SCALE, min_z), (max_y + SCALE, max_z + SCALE), (min_y, max_z + SCALE)]
        y_bricks.append(Polygon(y_path))

    if not test:
        file.close()

    # print(x_bricks)
    # p = gpd.GeoSeries(x_bricks)
    # p.plot()
    # plt.show()
    #
    # print(y_bricks)
    # p = gpd.GeoSeries(y_bricks)
    # p.plot()
    # plt.show()

    # bricks.sort(key=lambda a: (min(a[2]), min(a[1]), min(a[0])))

    # print(x_bricks[0].intersects(x_bricks[1]))
    # x_bricks[1] = translate(x_bricks[1], 0, -1)
    # print(x_bricks[0].intersects(x_bricks[1]))

    # print(x_bricks)
    # p = gpd.GeoSeries(x_bricks)
    # p.plot()
    # plt.show()

    # for b1 in x_bricks:
    #     for b2 in x_bricks:
    #         if b1 != b2 and b1.intersects(b2):
    #             print(f'{b1}   {b2}')

    move_down(x_bricks, y_bricks)
    print_bricks(x_bricks)
    print_bricks(y_bricks)

    return 0


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
