from util.util import timeit

def _extract_xy(vals: str, sep: str) -> (int, int):
    vals = vals.strip().split(',')
    x = "".join([c for c in vals[0].split(sep)[1] if c.isnumeric()])
    y = "".join([c for c in vals[1].split(sep)[1] if c.isnumeric()])
    return int(x), int(y)

def _solve(ax: int, ay: int, bx: int, by: int, prize_x: int, prize_y: int) -> int:
    a_count = round((prize_x * by - prize_y * bx) / (ax * by - ay * bx))
    b_count = round((ax * prize_y - ay * prize_x) / (ax * by - ay * bx))

    # Check if this is a valid solution
    if ax * a_count + bx * b_count == prize_x and ay * a_count + by * b_count == prize_y:
        return a_count * 3 + b_count
    return 0

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        params = line.split(':')
        if params[0] == 'Button A':
            ax, ay = _extract_xy(params[1], '+')

        if params[0] == 'Button B':
            bx, by = _extract_xy(params[1], '+')

        if params[0] == 'Prize':
            prize_x, prize_y = _extract_xy(params[1], '=')
            score += _solve(ax, ay, bx, by, prize_x, prize_y)

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        params = line.split(':')
        if params[0] == 'Button A':
            ax, ay = _extract_xy(params[1], '+')

        if params[0] == 'Button B':
            bx, by = _extract_xy(params[1], '+')

        if params[0] == 'Prize':
            prize_x, prize_y = _extract_xy(params[1], '=')
            score += _solve(ax, ay, bx, by, prize_x+10000000000000, prize_y+10000000000000)

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
