from util.util import timeit

bounds = (71,71)
invalid_path = 99_999

def valid_position(obstacles, pos):
    return 0 <= pos[0] < bounds[0] and 0 <= pos[1] < bounds[1] and pos not in obstacles

def _explore(pos):
    (x, y) = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def _bfs(obstacles, distance, levels):
    while edge := set(next_pos for pos in levels[-1]
                          for next_pos in _explore(pos) if valid_position(obstacles, next_pos) and next_pos not in distance):
        distance.update({ pos: len(levels) for pos in edge })
        levels += [edge]

    return distance

def _get_distance(obstacles, start, end):
    return _bfs(set(obstacles), { start: 0 }, [{start}]).get(end, invalid_path)

@timeit
def calculate_score_pt1(test: bool) -> int:
    global bounds
    iterations = 1024
    if test:
        file = open("test.txt", "r")
        iterations = 12
        bounds = (7,7)
    else:
        file = open("input.txt", "r")

    obstacles = []
    for line in file:
        l = line.split(',')
        obstacles.append((int(l[0].strip()), int(l[1].strip())))

    start = (0, 0)
    end = (bounds[0] - 1, bounds[1] - 1)
    return _get_distance(obstacles[:iterations], start, end)

@timeit
def calculate_score_pt2(test: bool) -> (int, int):
    global bounds
    if test:
        file = open("test.txt", "r")
        bounds = (7, 7)
    else:
        file = open("input.txt", "r")

    obstacles = []
    for line in file:
        l = line.split(',')
        obstacles.append((int(l[0].strip()), int(l[1].strip())))

    start = (0, 0)
    end = (bounds[0] - 1, bounds[1] - 1)
    for i in range(len(obstacles)):
        if _get_distance(obstacles[:i], start, end) == invalid_path:
            return obstacles[:i][-1]

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Results: {score}')