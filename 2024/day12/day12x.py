from util.util import timeit

plot_map = []
all_points = []

def _valid_point(x: int, y: int, char: str) -> bool:
    # Check that the location is within the map and that the char is the same
    if y < 0 or y >= len(plot_map) or x < 0 or x >= len(plot_map[y]) or plot_map[y][x] != char:
        return False
    return True

def _check_north(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x, y-1, char):
        return x, y-1
    return None

def _check_northeast(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x+1, y-1, char):
        return x+1, y-1
    return None

def _check_east(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x+1, y, char):
        return x+1, y
    return None

def _check_south(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x, y+1, char):
        return x, y+1
    return None

def _check_southeast(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x+1, y+1, char):
        return x+1, y+1
    return None

def _check_west(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x-1, y, char):
        return x-1, y
    return None

def _check_northwest(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x-1, y-1, char):
        return x-1, y-1
    return None

def _check_southwest(x: int, y: int, char: str) -> (int, int):
    if _valid_point(x-1, y+1, char):
        return x-1, y+1
    return None

def _find_plot_boundaries(pt, char):
    if pt in all_points:
        return [], 0

    all_points.append(pt)
    edge_count = 0
    points = []
    points.append(pt)

    n_pt = _check_north(pt[0], pt[1], char)
    e_pt = _check_east(pt[0], pt[1], char)
    s_pt = _check_south(pt[0], pt[1], char)
    w_pt = _check_west(pt[0], pt[1], char)
    dirs = [n_pt, e_pt, s_pt, w_pt]

    for dir in dirs:
        if dir:
            if dir not in all_points:
                pts, ct = _find_plot_boundaries(dir, char)
                points += pts
                edge_count += ct
        else:
            edge_count += 1

    # print(points)
    return points, edge_count

def _find_plot_boundaries2(pt, char):
    if pt in all_points:
        return [], 0

    all_points.append(pt)
    corner_count = 0
    points = []
    points.append(pt)

    n_pt = _check_north(pt[0], pt[1], char)
    ne_pt = _check_northeast(pt[0], pt[1], char)
    nw_pt = _check_northwest(pt[0], pt[1], char)
    e_pt = _check_east(pt[0], pt[1], char)
    s_pt = _check_south(pt[0], pt[1], char)
    se_pt = _check_southeast(pt[0], pt[1], char)
    sw_pt = _check_southwest(pt[0], pt[1], char)
    w_pt = _check_west(pt[0], pt[1], char)
    dirs = [n_pt, e_pt, s_pt, w_pt]

    for dir in dirs:
        if dir:
            if dir not in all_points:
                pts, ct = _find_plot_boundaries2(dir, char)
                points += pts
                corner_count += ct

    if ((n_pt is None and ne_pt is None and e_pt is None) or
        (e_pt is None and se_pt is None and s_pt is None) or
        (s_pt is None and sw_pt is None and w_pt is None) or
        (w_pt is None and nw_pt is None and n_pt is None) or
        (n_pt is not None and ne_pt is not None and e_pt is not None) or
        (e_pt is not None and se_pt is not None and s_pt is not None) or
        (s_pt is not None and sw_pt is not None and w_pt is not None) or
        (w_pt is not None and nw_pt is not None and n_pt is not None)):
        corner_count += 1


    # print(points)
    return points, corner_count

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    for line in file:
        plot_map.append([x for x in line.strip()])

    # print(plot_map)

    plots = []
    score = 0
    for y, line in enumerate(plot_map):
        for x, char in enumerate(line):
            if (x, y) in all_points:
                continue

            pts, ct = _find_plot_boundaries((x, y), char)
            plots.append(pts)
            score += ct * len(pts)
            # print(f"{char} has a score of {len(pts)} * {ct} = {ct * len(pts)}")

    return score

@timeit
def calculate_score_pt2() -> int:
    plots = []
    score = 0
    for y, line in enumerate(plot_map):
        for x, char in enumerate(line):
            if (x, y) in all_points:
                continue

            pts, ct = _find_plot_boundaries2((x, y), char)
            plots.append(pts)
            score += ct * len(pts)
            # print(f"{char} has a score of {len(pts)} * {ct} = {ct * len(pts)}")

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=True)
    print(f'Score: {score}')

    score = calculate_score_pt2()
    print(f'Score: {score}')
