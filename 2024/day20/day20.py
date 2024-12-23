from functools import cache
from heapq import heappop, heappush
from itertools import combinations

from util.util import timeit

maze = []
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
threshold = 100

def valid_position(pos):
    return 0 <= pos[0] < len(maze[0]) and 0 <= pos[1] < len(maze)

@cache
def take_step(location, direction):
    next_location = (location[0] + direction[0], location[1] + direction[1])
    if valid_position(next_location):
        if maze[next_location[1]][next_location[0]] in '.E':
            return next_location
    return -1, -1

@cache
def take_cheat_step(location, direction):
    next_location = (location[0] + direction[0], location[1] + direction[1])
    if valid_position(next_location):
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
    final_path = []
    costs[start_location[1]] = 0
    while path_queue:
        cost, cur_pos, from_direction, path = heappop(path_queue)
        if cur_pos[0] == end_location[0] and cur_pos[1] == end_location[1]:
            cost_list.append(cost)  # We've reached the end
            final_path = path
            continue
        if cur_pos in path:
            continue  # We've already been here
        path.append(cur_pos)
        for direction in DIRECTIONS:
            if direction == (from_direction[0] * -1, from_direction[1] * -1):
                continue  # We can't go backwards
            next_pos = take_step(cur_pos, direction)

            if valid_position(next_pos):
                new_cost = cost + 1
                if costs.get(next_pos, 1_000_000) < new_cost:
                    continue  # If lower cost path already exists, ignore this path
                costs[next_pos] = new_cost
                heappush(path_queue, (new_cost, next_pos, direction, path.copy()))


    cheat_ct = {}
    for location in final_path:
        cost = costs.get(location, None)
        for direction in DIRECTIONS:
            next_pos1 = take_cheat_step(location, direction)
            next_pos2 = take_cheat_step(next_pos1, direction)

            non_cheat_cost = costs.get(next_pos2, None)
            if non_cheat_cost and non_cheat_cost > cost + 2:
                savings = non_cheat_cost - (cost + 2)
                cheat_ct[savings] = cheat_ct.get(savings, 0) + 1

    score1 = 0
    for savings, ct in cheat_ct.items():
        if savings >= threshold:
            score1 += ct

    cheats = {}
    cheat_ct = {}
    x = combinations(final_path, 2)
    for l, r in x:
        delta_x = abs(l[0] - r[0])
        delta_y = abs(l[1] - r[1])
        cost = costs.get(l, None)
        non_cheat_cost = costs.get(r, None)

        if non_cheat_cost and non_cheat_cost > cost + delta_x + delta_y and delta_x + delta_y <= 20:
            if (l, r) not in cheats:
                savings = non_cheat_cost - (cost + delta_x + delta_y)
                cheat_ct[savings] = cheat_ct.get(savings, 0) + 1
                cheats[(l, r)] = savings

    score2 = 0
    cheat_ct = dict(sorted(cheat_ct.items()))
    for savings, ct in cheat_ct.items():
        if savings >= threshold:
            score2 += ct
            print(ct, "that save", savings, "seconds")

    return score1, score2

@timeit
def calculate_score_pt1(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
        global threshold
        threshold = 50
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
    score = calculate_score_pt1(test=True)
    print(f'Score: {score}')