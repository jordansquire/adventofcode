from functools import cache
from heapq import heappop, heappush
from util.util import timeit

test_data = [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#',
]
trail_map = []
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def valid_position(pos):
    return 0 <= pos[0] < len(trail_map[0]) and 0 <= pos[1] < len(trail_map)


@cache
def take_step(location, direction):
    next_location = (location[0] + direction[0], location[1] + direction[1])
    if valid_position(next_location):
        if trail_map[next_location[1]][next_location[0]] == '.':
            return next_location
        if trail_map[next_location[1]][next_location[0]] == '>' and direction == (1, 0):
            return next_location
        if trail_map[next_location[1]][next_location[0]] == '<' and direction == (-1, 0):
            return next_location
        if trail_map[next_location[1]][next_location[0]] == '^' and direction == (0, -1):
            return next_location
        if trail_map[next_location[1]][next_location[0]] == 'v' and direction == (0, 1):
            return next_location
    return -1, -1


def discover_path(start_location, end_location):
    path_queue = [start_location]  # cost, x, y, from_direction
    costs = {}
    cost_list = []
    paths = []
    while path_queue:
        cost, x, y, from_direction, path = heappop(path_queue)
        if x == end_location[0] and y == end_location[1]:
            cost_list.append(cost)  # We've reached the end
            paths.append(path)
            continue
        if (x, y) in path:
            continue  # We've already been here
        path.append((x, y))
        for direction in DIRECTIONS:
            if direction == (from_direction[0] * -1, from_direction[1] * -1):
                continue  # We can't go this way
            next_x, next_y = take_step((x, y), direction)

            if valid_position((next_x, next_y)):
                new_cost = cost + 1
                if costs.get((next_x, next_y, direction), 0) > new_cost:
                    continue  # If higher cost path already exists, ignore this path
                costs[(next_x, next_y, direction)] = new_cost
                heappush(path_queue, (new_cost, next_x, next_y, direction, path.copy()))

    # print_map(path)
    return max(cost_list)


def print_map(locations):
    for y in range(len(trail_map)):
        line = ''
        for x in range(len(trail_map[0])):
            if (x, y) in locations:
                line += 'O'
            else:
                line += trail_map[y][x]
        print(line)


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        trail_map.append(line.strip())

    if not test:
        file.close()

    start_location = (0, 0, trail_map[0].index('.'), (0, 0), [])
    end_location = (trail_map[len(trail_map)-1].index('.'), len(trail_map)-1)
    return discover_path(start_location, end_location)


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
