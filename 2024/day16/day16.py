from functools import cache
from heapq import heappop, heappush
from util.util import timeit

maze = []
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def valid_position(pos):
    return 0 <= pos[0] < len(maze[0]) and 0 <= pos[1] < len(maze)

@cache
def take_step(location, direction):
    next_location = (location[0] + direction[0], location[1] + direction[1])
    if valid_position(next_location):
        if maze[next_location[1]][next_location[0]] in '.E':
            return next_location
    return -1, -1

def print_map(locations):
    for y in range(len(maze)):
        line = ''
        for x in range(len(maze[0])):
            if (x, y) in locations:
                line += 'O'
            else:
                line += maze[y][x]
        print(line)

def discover_path(start_location, end_location):
    path_queue = [start_location]  # cost, (x, y), from_direction, path
    costs = {}
    cost_list = []
    paths = []
    while path_queue:
        cost, cur_pos, from_direction, path = heappop(path_queue)
        if cur_pos[0] == end_location[0] and cur_pos[1] == end_location[1]:
            cost_list.append(cost)  # We've reached the end
            paths.append(path)
            continue
        if cur_pos in path:
            continue  # We've already been here
        path.append(cur_pos)
        for direction in DIRECTIONS:
            if direction == (from_direction[0] * -1, from_direction[1] * -1):
                continue  # We can't go backwards
            next_pos = take_step(cur_pos, direction)

            if valid_position(next_pos):
                if direction == from_direction:
                    new_cost = cost + 1
                else:
                    new_cost = cost + 1001
                if costs.get((next_pos, direction), 1_000_000) < new_cost:
                    continue  # If lower cost path already exists, ignore this path
                costs[(next_pos, direction)] = new_cost
                heappush(path_queue, (new_cost, next_pos, direction, path.copy()))

    min_cost = min(cost_list)
    seats = set()
    for i, path in enumerate(paths):
        if cost_list[i] == min_cost:
            for location in path:
                seats.add(location)

    return min_cost, len(seats) + 1

@timeit
def calculate_score_pt1(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    start_pos = None
    end_pos = None
    for y, line in enumerate(file):
        row = []
        for x, char in enumerate(line.strip()):
            if char == "S":
                start_pos = (x, y)
            if char == "E":
                end_pos = (x, y)
            row.append(char)
        maze.append(row)

    start_location = (0, start_pos, DIRECTIONS[1], [])  # cost, (x, y), from_direction, path
    return discover_path(start_location, end_pos)

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')
