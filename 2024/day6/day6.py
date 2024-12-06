from enum import Enum
from util.util import timeit

start_loc = []
loc_map = []
path = set()

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

def _has_obstacle(char: str) -> bool:
    return char == '#'

def _navigate_north(x: int, y: int) -> (int, int):
    if y == 0:
        return None
    if _has_obstacle(loc_map[y-1][x]):
        return x, y
    else:
        return x, y-1

def _navigate_east(x: int, y: int) -> (int, int):
    if x == len(loc_map[y]) - 1:
        return None
    if _has_obstacle(loc_map[y][x+1]):
        return x, y
    else:
        return x+1, y

def _navigate_south(x: int, y: int) -> (int, int):
    if y == len(loc_map) - 1:
        return None
    if _has_obstacle(loc_map[y+1][x]):
        return x, y
    else:
        return x, y+1

def _navigate_west(x: int, y: int) -> (int, int):
    if x == 0:
        return None
    if _has_obstacle(loc_map[y][x-1]):
        return x, y
    else:
        return x-1, y

def _navigate(direction: Direction, current_loc: (int, int)) -> (int, int):
    if direction == Direction.NORTH:
        return _navigate_north(current_loc[0], current_loc[1])
    elif direction == Direction.EAST:
        return _navigate_east(current_loc[0], current_loc[1])
    elif direction == Direction.SOUTH:
        return _navigate_south(current_loc[0], current_loc[1])
    elif direction == Direction.WEST:
        return _navigate_west(current_loc[0], current_loc[1])

def _handle_obstacle(direction: Direction, current_loc: (int, int), next_loc: (int, int)) -> Direction:
    # If the location didn't change we hit an obstacle, change direction
    if next_loc[0] == current_loc[0] and next_loc[1] == current_loc[1]:
        if direction == Direction.WEST:
            return Direction.NORTH
        else:
            return Direction(direction.value + 1)
    else:
        return direction

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("input_test.txt", "r")
    else:
        file = open("input.txt", "r")

    for row_num, line in enumerate(file):
        loc_map.append(line.strip())
        try:
            start_loc.append(line.index('^'))
            start_loc.append(row_num)

        except ValueError:
            pass

    current_loc = (start_loc[0], start_loc[1])
    loc_map[current_loc[1]] = loc_map[current_loc[1]][:current_loc[0]] + 'X' + loc_map[current_loc[1]][current_loc[0]+1:]

    direction = Direction.NORTH
    while current_loc is not None:
        path.add(current_loc)

        next_loc = _navigate(direction, current_loc)

        # None means we exited the map
        if next_loc is None:
            break

        direction = _handle_obstacle(direction, current_loc, next_loc)
        loc_map[next_loc[1]] = loc_map[next_loc[1]][:next_loc[0]] + 'X' + loc_map[next_loc[1]][next_loc[0]+1:]
        current_loc = next_loc

    return len(path)

def _check_for_loops() -> int:
    cl1 = cl2 = (start_loc[0], start_loc[1])
    d1 = d2 = Direction.NORTH
    while cl1 is not None and cl2 is not None:
        # Navigate both fast and slow
        nl1 = _navigate(d1, cl1)
        nl2 = _navigate(d2, cl2)

        if nl2 is None:
            return 0  # None means we exited the map

        d1 = _handle_obstacle(d1, cl1, nl1)
        d2 = _handle_obstacle(d2, cl2, nl2)

        # Navigate fast again
        cl2 = nl2
        nl2 = _navigate(d2, cl2)

        if nl2 is None:
            return 0  # None means we exited the map

        d2 = _handle_obstacle(d2, cl2, nl2)

        if nl1 == nl2 and d1 == d2:
            return 1  # If fast and slow are on the same spot heading the same direction we are in a loop

        cl1 = nl1
        cl2 = nl2

@timeit
def calculate_score_pt2() -> int:
    score = 0
    for loc in path:
        if loc == (start_loc[0], start_loc[1]):
            continue
        # Try adding an obstacle on the path and then check for loops
        loc_map[loc[1]] = loc_map[loc[1]][:loc[0]] + '#' + loc_map[loc[1]][loc[0] + 1:]
        score += _check_for_loops()

        # Remove the obstacle
        loc_map[loc[1]] = loc_map[loc[1]][:loc[0]] + 'X' + loc_map[loc[1]][loc[0] + 1:]
    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2()
    print(f'Score: {score}')
