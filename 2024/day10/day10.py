from util.util import timeit

topo_map = []
trailheads = []
summit_counts = {}

def _valid_location(x: int, y: int, val: int) -> bool:
    # Check that the location is within the map and that the value is an increase of one
    if y < 0 or y >= len(topo_map) or x < 0 or x >= len(topo_map[y]) or topo_map[y][x] != val+1:
        return False
    return True

def _is_summit(x: int, y: int) -> bool:
    return topo_map[y][x] == 9

def _navigate_north(x: int, y: int, val: int) -> (int, int):
    if _valid_location(x, y-1, val):
        return x, y-1
    return None

def _navigate_east(x: int, y: int, val: int) -> (int, int):
    if _valid_location(x+1, y, val):
        return x+1, y
    return None

def _navigate_south(x: int, y: int, val: int) -> (int, int):
    if _valid_location(x, y+1, val):
        return x, y+1
    return None

def _navigate_west(x: int, y: int, val: int) -> (int, int):
    if _valid_location(x-1, y, val):
        return x - 1, y
    return None

def _navigate_distinct(start: (int, int), location: (int, int), val: int):
    # Find the distinct summits accessible by a trailhead
    if val == 9 and _is_summit(location[0], location[1]):
        summit_counts[start].add(location)
        return

    n_loc = _navigate_north(location[0], location[1], val)
    e_loc = _navigate_east(location[0], location[1], val)
    s_loc = _navigate_south(location[0], location[1], val)
    w_loc = _navigate_west(location[0], location[1], val)

    if n_loc:
        _navigate_distinct(start, n_loc, val+1)
    if e_loc:
        _navigate_distinct(start, e_loc, val+1)
    if s_loc:
        _navigate_distinct(start, s_loc, val+1)
    if w_loc:
        _navigate_distinct(start, w_loc, val+1)
    return

def _navigate_all(location: (int, int), val: int) -> int:
    # Count the number of paths that lead to summits
    if val == 9 and _is_summit(location[0], location[1]):
        return 1

    n_loc = _navigate_north(location[0], location[1], val)
    e_loc = _navigate_east(location[0], location[1], val)
    s_loc = _navigate_south(location[0], location[1], val)
    w_loc = _navigate_west(location[0], location[1], val)

    score = 0
    if n_loc:
        score += _navigate_all(n_loc, val+1)
    if e_loc:
        score += _navigate_all(e_loc, val+1)
    if s_loc:
        score += _navigate_all(s_loc, val+1)
    if w_loc:
        score += _navigate_all(w_loc, val+1)
    return score

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        map_line = []
        for x, char in enumerate(line.strip()):
            if char == '.':
                char = -1
            map_line.append(int(char))
            if char == "0":
                trailheads.append((x, y))
        topo_map.append(map_line)

    for trail in trailheads:
        summit_counts[trail] = set()
        _navigate_distinct((trail[0], trail[1]), (trail[0], trail[1]),0)

    score = 0
    for paths in summit_counts:
        score += len(summit_counts[paths])
    return score


@timeit
def calculate_score_pt2() -> int:
    score = 0
    for trail in trailheads:
        score += _navigate_all((trail[0], trail[1]), 0)

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2()
    print(f'Score: {score}')
