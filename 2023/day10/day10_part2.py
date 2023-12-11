from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from util.util import timeit

test_data1 = [
    '.....',
    'F-7..',
    '|IL7.',
    'L-7|.',
    '..||.',
    '.SJ|.',
    '.|I|.',
    '.L-J.',
    '.....',
]
test_data2 = [
    '...........',
    '.S-------7.',
    '.|F-----7|.',
    '.||OOOOO||.',
    '.||OOOOO||.',
    '.|L-7OF-J|.',
    '.|II|O|II|.',
    '.L--JOL--J.',
    '.....O.....',
]
test_data3 = [
    '..........',
    '.S------7.',
    '.|F----7|.',
    '.||OOOO||.',
    '.||OOOO||.',
    '.|L-7F-J|.',
    '.|II||II|.',
    '.L--JL--J.',
    '..........',
]
test_data4 = [
    'OF----7F7F7F7F-7OOOO',
    'O|F--7||||||||FJOOOO',
    'O||OFJ||||||||L7OOOO',
    'FJL7L7LJLJ||LJIL-7OO',
    'L--JOL7IIILJS7F-7L7O',
    'OOOOF-JIIF7FJ|L7L7L7',
    'OOOOL7IF7||L7|IL7L7|',
    'OOOOO|FJLJ|FJ|F7|OLJ',
    'OOOOFJL-7O||O||||OOO',
    'OOOOL---JOLJOLJLJOOO',
]
test_data5 = [
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJIF7FJ-',
    'L---JF-JLJIIIIFJLJJ7',
    '|F|F-JF---7IIIL7L|7|',
    '|FFJF7L7F-JF7IIL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L',
]

path_map = []


def valid_location(location) -> bool:
    return 0 <= location['x'] < len(path_map[0]) and 0 <= location['y'] < len(path_map)


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


def get_location_key(location):
    return f"{location['x']}_{location['y']}"


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data5
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

    cur_location = start_loc.copy()
    directions = ["north", "east", "south", "west"]
    for cur_direction in directions:
        step = 0
        path_found = False
        complete_path = [get_location_key(start_loc)]
        coords = []
        while True:
            next_location, next_direction = navigate(cur_location, cur_direction)
            complete_path.append(get_location_key(cur_location))
            coords.append((cur_location['x'], cur_location['y']))

            if next_location is None:
                break

            if path_map[next_location['y']][next_location['x']] == 'S':
                path_found = True
                break

            # print(f"{path_map[next_location['y']][next_location['x']]} {step}")

            cur_location = next_location
            cur_direction = next_direction

        if path_found:
            polygon = Polygon(coords)
            for y in range(0, len(path_map)):
                for x in range(0, len(path_map[0])):
                    location = {'x': x, 'y': y}
                    if get_location_key(location) in complete_path:
                        continue
                    point = Point(x, y)
                    step += polygon.contains(point)
            return step
    return 0


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
