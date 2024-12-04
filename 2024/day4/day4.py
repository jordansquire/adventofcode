from util.util import timeit

test_data1 = [
    'MMMSXXMASM',
    'MSAMXMSMSA',
    'AMXSXMAAMM',
    'MSAMASMSMX',
    'XMASAMXAMM',
    'XXAMMXXAMA',
    'SMSMSASXSS',
    'SAXAMASAAA',
    'MAMMMXMMMM',
    'MXMXAXMASX',
]

def transpose_diagonally(matrix, reverse=False):
    """Rotates a list of lists by 45 degrees"""

    rows = len(matrix)
    cols = len(matrix[0])

    # Create a new matrix to store the rotated elements
    rotated = [[' ' for _ in range(rows + cols - 1)] for _ in range(rows + cols - 1)]

    # Fill the new matrix with rotated elements
    for i in range(rows):
        for j in range(cols):
            if reverse:
                rotated[i + j][cols - 1 - j + i] = matrix[i][cols - 1 - j]
            else:
                rotated[i + j][cols - 1 - j + i] = matrix[i][j]

    # Remove empty rows and columns
    result = [row for row in rotated if any(x != ' ' for x in row)]
    result = [[x for x in row if x != ' '] for row in result]

    return result

def _count_words(puzzle):
    points = 0
    for line in puzzle:
        line = "".join(line)
        points += line.count('XMAS') + line.count('SAMX')
    return points

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data1
    else:
        file = open("input.txt", "r")

    puzzle = []
    for line in file:
        puzzle.append(line.strip())

    score = 0
    score += _count_words(puzzle)

    transposed_puzzle = list(zip(*puzzle))
    score += _count_words(transposed_puzzle)

    transposed_puzzle = transpose_diagonally(puzzle)
    score += _count_words(transposed_puzzle)

    transposed_puzzle = transpose_diagonally(puzzle, reverse=True)
    score += _count_words(transposed_puzzle)

    return score

def _get_up_left_char(map, x, y):
    if x == 0 or y == 0:
        return None
    c = map[y-1][x-1]
    if c == 'M' or c == 'S':
        return c
    return None

def _get_up_right_char(map, x, y):
    if x == len(map[0]) - 1 or y == 0:
        return None
    c = map[y-1][x+1]
    if c == 'M' or c == 'S':
        return c
    return None

def _get_down_left_char(map, x, y):
    if x == 0 or y == len(map) - 1:
        return None
    c = map[y+1][x-1]
    if c == 'M' or c == 'S':
        return c
    return None

def _get_down_right_char(map, x, y):
    if x == len(map[0]) - 1 or y == len(map) - 1:
        return None
    c = map[y+1][x+1]
    if c == 'M' or c == 'S':
        return c
    return None

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data1
    else:
        file = open("input.txt", "r")

    puzzle = []
    for line in file:
        puzzle.append(line.strip())

    score = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] != 'A':
                continue

            tl = _get_up_left_char(puzzle, x, y)
            tr = _get_up_right_char(puzzle, x, y)
            bl = _get_down_left_char(puzzle, x, y)
            br = _get_down_right_char(puzzle, x, y)

            if tl and tr and bl and br:
                if ((tl == tr and bl == br and tl != bl)
                        or (tr == br and tl == bl and tr != bl)):
                    score += 1

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
