from util.util import timeit

box_map = []

def _get_next_pos(cur_pos: (int, int), direction: str) -> (int, int):
    if direction == '^':
        return cur_pos[0], cur_pos[1] - 1
    if direction == '>':
        return cur_pos[0] + 1, cur_pos[1]
    if direction == 'v':
        return cur_pos[0], cur_pos[1] + 1
    if direction == '<':
        return cur_pos[0] - 1, cur_pos[1]

def _move_box(pos: (int, int), direction: str) -> bool:
    next_pos = _get_next_pos(pos, direction)
    char = box_map[next_pos[1]][next_pos[0]]
    move = False
    if char == '#':
        return False
    if char == '.':
        box_map[next_pos[1]][next_pos[0]] = 'O'
        return True
    if char == 'O':
        move = _move_box(next_pos, direction)

    if move:
        box_map[next_pos[1]][next_pos[0]] = 'O'
    return move

def _move(cur_pos: (int, int), direction: str) -> (int, int):
    next_pos = _get_next_pos(cur_pos, direction)
    char = box_map[next_pos[1]][next_pos[0]]
    if char == '#':
        return cur_pos
    if char == '.':
        return next_pos
    if char == 'O':
        if _move_box(next_pos, direction):
            return next_pos
        else:
            return cur_pos

def _print_map():
    for line in box_map:
        print(''.join(line))

def _calculate_score() -> int:
    score = 0
    for y, line in enumerate(box_map):
        for x, char in enumerate(line):
            if char == 'O':
                score += 100 * y + x
    return score

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    start_pos = None
    map = True
    instructions = ""
    for y, line in enumerate(file):
        if line.strip() == "":
            map = False
            continue

        if map:
            row = []
            for x, char in enumerate(line.strip()):
                if char == "@":
                    start_pos = (x, y)
                row.append(char)
            box_map.append(row)
        else:
            instructions += line.strip()

    cur_pos = start_pos
    for instr in instructions:
        next_pos = _move(cur_pos, instr)
        if cur_pos != next_pos:
            box_map[next_pos[1]][next_pos[0]] = '@'
            box_map[cur_pos[1]][cur_pos[0]] = '.'

        cur_pos = next_pos

    _print_map()
    return _calculate_score()


if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')