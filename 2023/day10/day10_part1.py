from util.util import timeit

test_data1 = [
    '-L|F7',
    '7S-7|',
    'L|7||',
    '-L-J|',
    'L|-JF',
]

test_data2 = [
    '7-F7-',
    '.FJ|7',
    'SJLL7',
    '|F--J',
    'LJ.LJ',
]

path_map = []


def valid_location(location) -> bool:
    return 0 <= location['x'] < len(path_map[0]) and 0 <= location['y'] < len(path_map[0])


def navigate_north(location):
    n_location = {'x': location['x'], 'y': location['y'] - 1}
    from_direction = 'south'
    if not valid_location(n_location):
        return None, None, None

    n_char = path_map[n_location['y']][n_location['x']]
    if n_char == '7':
        return n_location, from_direction, "west"
    if n_char == '|':
        return n_location, from_direction, "north"
    if n_char == 'F':
        return n_location, from_direction, "east"
    if n_char == 'S':
        return n_location, from_direction, "north"

    return None, None, None


def navigate_east(location):
    e_location = {'x': location['x'] + 1, 'y': location['y']}
    from_direction = 'west'
    if not valid_location(e_location):
        return None, None, None

    e_char = path_map[e_location['y']][e_location['x']]
    if e_char == '7':
        return e_location, from_direction, 'south'
    if e_char == '-':
        return e_location, from_direction, 'east'
    if e_char == 'J':
        return e_location, from_direction, 'north'
    if e_char == 'S':
        return e_location, from_direction, "east"

    return None, None, None


def navigate_south(location):
    s_location = {'x': location['x'], 'y': location['y'] + 1}
    from_direction = 'north'
    if not valid_location(s_location):
        return None, None, None

    s_char = path_map[s_location['y']][s_location['x']]
    if s_char == 'J':
        return s_location, from_direction, 'west'
    if s_char == '|':
        return s_location, from_direction, 'south'
    if s_char == 'L':
        return s_location, from_direction, 'east'
    if s_char == 'S':
        return s_location, from_direction, "south"

    return None, None, None


def navigate_west(location):
    w_location = {'x': location['x'] - 1, 'y': location['y']}
    from_direction = 'east'
    if not valid_location(w_location):
        return None, None, None

    w_char = path_map[w_location['y']][w_location['x']]
    if w_char == 'L':
        return w_location, from_direction, 'north'
    if w_char == '-':
        return w_location, from_direction, 'west'
    if w_char == 'F':
        return w_location, from_direction, 'south'
    if w_char == 'S':
        return w_location, from_direction, "west"

    return None, None, None


def navigate(location, direction):
    if direction == 'north' or direction == '':
        next_location, _, next_direction = navigate_north(location)
        if next_location is not None:
            return next_location, next_direction

    if direction == 'east' or direction == '':
        next_location, _, next_direction = navigate_east(location)
        if next_location is not None:
            return next_location, next_direction

    if direction == 'south' or direction == '':
        next_location, _, next_direction = navigate_south(location)
        if next_location is not None:
            return next_location, next_direction

    if direction == 'west' or direction == '':
        next_location, _, next_direction = navigate_west(location)
        if next_location is not None:
            return next_location, next_direction

    return None, None


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data2
    else:
        file = open("input.txt", "r")

    start_loc = None
    for row_num, line in enumerate(file):
        path_map.append(line.strip())
        try:
            start_loc = {'x': line.index('S'), 'y': row_num}
        except ValueError:
            pass

    if not test:
        file.close()

    north_path = []
    east_path = []
    south_path = []
    west_path = []
    cur_location = start_loc.copy()
    directions = ["north", "east", "south", "west"]
    for cur_direction in directions:
        step = 0
        while True:
            next_location, next_direction = navigate(cur_location, cur_direction)

            if next_location is None:
                break

            step += 1
            if path_map[next_location['y']][next_location['x']] == 'S':
                return int(step / 2)

            # print(f"{path_map[next_location['y']][next_location['x']]} {step}")

            cur_location = next_location
            cur_direction = next_direction


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
