from util.util import timeit

big_box_map = []

def _get_next_pos(cur_pos: (int, int), direction: str) -> (int, int):
    if direction == '^':
        return cur_pos[0], cur_pos[1] - 1
    if direction == '>':
        return cur_pos[0] + 1, cur_pos[1]
    if direction == 'v':
        return cur_pos[0], cur_pos[1] + 1
    if direction == '<':
        return cur_pos[0] - 1, cur_pos[1]

def _move_box(pos: (int, int), direction: str, depth: int):
    boxes = []
    cur_char = big_box_map[pos[1]][pos[0]]
    if direction in '<>':
        side_pos = _get_next_pos(pos, direction)

        if cur_char == '#':
            return None
        if cur_char == '.':
            return []
        if cur_char in '[]':
            boxes += [side_pos, pos]

            next_pos = _get_next_pos(side_pos, direction)
            box = _move_box(next_pos, direction, depth+1)
            if box is not None:
                boxes = box + boxes
            else:
                return None
    else:
        # Find all boxes
        if cur_char == '#':
            return None
        if cur_char == '.':
            return []
        if cur_char in '[]':
            if cur_char == ']':
                side_pos = _get_next_pos(pos, '<')
            else:
                side_pos = _get_next_pos(pos, '>')

            boxes += [pos, side_pos]
            next_pos = _get_next_pos(pos, direction)
            box = _move_box(next_pos, direction, depth + 1)
            if box is not None:
                boxes = box + boxes
            else:
                return None

            next_side_pos = _get_next_pos(side_pos, direction)
            if big_box_map[next_pos[1]][next_pos[0]] != cur_char:
                box = _move_box(next_side_pos, direction, depth + 1)
                if box is not None:
                    boxes = box + boxes
                else:
                    return None

    if depth == 0:
        for box in boxes:
            next_pos = _get_next_pos(box, direction)
            big_box_map[next_pos[1]][next_pos[0]] = big_box_map[box[1]][box[0]]
            big_box_map[box[1]][box[0]] = '.'
    if len(boxes) == 0:
        return []
    return boxes


def _move(cur_pos: (int, int), direction: str) -> (int, int):
    next_pos = _get_next_pos(cur_pos, direction)
    char = big_box_map[next_pos[1]][next_pos[0]]
    if char == '#':
        return cur_pos
    if char == '.':
        return next_pos
    if char in '[]':
        if _move_box(next_pos, direction, 0) is not None:
            return next_pos
        else:
            return cur_pos

def _print_map():
    for line in big_box_map:
        print(''.join(line))

def _calculate_score() -> int:
    score = 0
    for y, line in enumerate(big_box_map):
        for x, char in enumerate(line):
            if char == '[':
                score += 100 * y + x
    return score

@timeit
def calculate_score(test: bool) -> int:
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
                    start_pos = (x*2, y)
                    row.append(char)
                    row.append('.')
                if char == "#" or char == '.':
                    row.append(char)
                    row.append(char)
                if char == 'O':
                    row.append('[')
                    row.append(']')
            big_box_map.append(row)
        else:
            instructions += line.strip()

    cur_pos = start_pos
    for instr in instructions:
        next_pos = _move(cur_pos, instr)
        if cur_pos != next_pos:
            big_box_map[next_pos[1]][next_pos[0]] = '@'
            big_box_map[cur_pos[1]][cur_pos[0]] = '.'

        cur_pos = next_pos
    _print_map()
    return _calculate_score()


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
