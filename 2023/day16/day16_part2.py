from util.util import timeit

test_data = [
    '.|...\\....',
    '|.-.\\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....',
]


mirror_map = []
cursors = []


def valid_location(location) -> bool:
    return 0 <= location[0] < len(mirror_map[0]) and 0 <= location[1] < len(mirror_map)


def navigate_north(location):
    next_location = (location[0], location[1] - 1)
    if not valid_location(next_location):
        return None, None

    char = mirror_map[next_location[1]][next_location[0]]
    if char in ('.', '|'):
        return next_location, "north"
    if char == '\\':
        return next_location, "west"
    if char == '/':
        return next_location, "east"
    if char == '-':
        cursors.append((next_location, "east"))
        return next_location, "west"

    return None, None


def navigate_east(location):
    next_location = (location[0] + 1, location[1])
    if not valid_location(next_location):
        return None, None

    char = mirror_map[next_location[1]][next_location[0]]
    if char in ('.', '-'):
        return next_location, "east"
    if char == '\\':
        return next_location, "south"
    if char == '/':
        return next_location, "north"
    if char == '|':
        cursors.append((next_location, "north"))
        return next_location, "south"

    return None, None


def navigate_south(location):
    next_location = (location[0], location[1] + 1)
    if not valid_location(next_location):
        return None, None

    char = mirror_map[next_location[1]][next_location[0]]
    if char in ('.', '|'):
        return next_location, "south"
    if char == '\\':
        return next_location, "east"
    if char == '/':
        return next_location, "west"
    if char == '-':
        cursors.append((next_location, "east"))
        return next_location, "west"

    return None, None


def navigate_west(location):
    next_location = (location[0] - 1, location[1])
    if not valid_location(next_location):
        return None, None

    char = mirror_map[next_location[1]][next_location[0]]
    if char in ('.', '-'):
        return next_location, "west"
    if char == '\\':
        return next_location, "north"
    if char == '/':
        return next_location, "south"
    if char == '|':
        cursors.append((next_location, "north"))
        return next_location, "south"

    return None, None


def navigate(location, direction):
    if direction == 'north':
        return navigate_north(location)

    if direction == 'east':
        return navigate_east(location)

    if direction == 'south':
        return navigate_south(location)

    if direction == 'west':
        return navigate_west(location)

    return None, None


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for row_num, line in enumerate(file):
        mirror_map.append(line.strip())

    if not test:
        file.close()

    score = 0
    x_max = len(mirror_map[0])
    y_max = len(mirror_map)
    edges = set()
    for x_edges in range(0, x_max):
        edges.add((x_edges, -1))
        edges.add((x_edges, y_max))
    for y_edges in range(0, y_max):
        edges.add((-1, y_edges))
        edges.add((x_max, y_edges))

    for edge in edges:
        location_history = set()
        energized_locations = set()
        cursors.clear()
        repeated_count = 0

        if edge[0] == -1:
            cursors.append(navigate_east(edge))
        if edge[0] == x_max:
            cursors.append(navigate_west(edge))
        if edge[1] == -1:
            cursors.append(navigate_south(edge))
        if edge[1] == y_max:
            cursors.append(navigate_north(edge))

        while len(cursors) > 0:
            next_location, next_direction = navigate(cursors[0][0], cursors[0][1])
            energized_locations.add(cursors[0][0])

            if (cursors[0][0], cursors[0][1]) not in location_history:
                location_history.add((cursors[0][0], cursors[0][1]))
            else:
                repeated_count += 1

            if next_location is None or repeated_count > 2:
                cursors.pop(0)
                repeated_count = 0
                continue

            cursors[0] = (next_location, next_direction)

        if len(energized_locations) > score:
            score = len(energized_locations)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
