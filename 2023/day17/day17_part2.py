from heapq import heappop, heappush
from util.util import timeit

test_data = [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533',
]
city_map = []
MAX_DISTANCE = 10
MIN_DISTANCE = 4


def valid_position(pos):
    return 0 <= pos[0] < len(city_map[0]) and 0 <= pos[1] < len(city_map)


def valid_direction(direction, next_direction):
    if direction in 'NS' and next_direction in 'NS':
        return False
    if direction in 'EW' and next_direction in 'EW':
        return False
    return True


def discover_path():
    path_queue = [(0, 0, 0, 'X')]  # cost, x, y, from_direction
    visited = set()
    costs = {}
    while path_queue:
        cost, x, y, from_direction = heappop(path_queue)
        if x == len(city_map[0]) - 1 and y == len(city_map) - 1:  # goal x, goal y
            return cost  # We've reached the end
        if (x, y, from_direction) in visited:
            continue  # We've already been here
        visited.add((x, y, from_direction))
        for direction in ('N', 'E', 'S', 'W'):
            cost_increase = 0
            if not valid_direction(direction, from_direction):
                continue  # We can't go this way
            for distance in range(1, MAX_DISTANCE+1):
                next_x = x
                next_y = y
                if direction == 'E':
                    next_x += distance
                if direction == 'W':
                    next_x -= distance
                if direction == 'S':
                    next_y += distance
                if direction == 'N':
                    next_y -= distance

                if valid_position((next_x, next_y)):
                    cost_increase += int(city_map[next_y][next_x])
                    if distance < MIN_DISTANCE:
                        continue  # We must move at least MIN_DISTANCE
                    new_cost = cost + cost_increase
                    if costs.get((next_x, next_y, direction), 1e99) <= new_cost:
                        continue  # If lower cost path already exists, ignore this path
                    costs[(next_x, next_y, direction)] = new_cost
                    heappush(path_queue, (new_cost, next_x, next_y, direction))


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for row_num, line in enumerate(file):
        city_map.append(line.strip())

    if not test:
        file.close()

    return discover_path()


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
