from util.util import timeit

DIRECTIONS = ['^', '>', 'v', '<']

key_pad = {
    'A': {'^': '3', '<': '0'},
    '0': {'^': '2', '>': 'A'},
    '1': {'^': '4', '>': '2'},
    '2': {'^': '5', '>': '3', 'v': '0', '<': '1'},
    '3': {'^': '6', 'v': 'A', '<': '2'},
    '4': {'^': '7', '>': '5', 'v': '1'},
    '5': {'^': '8', '>': '6', 'v': '2', '<': '1'},
    '6': {'^': '9', 'v': '3', '<': '5'},
    '7': {'>': '8', 'v': '4'},
    '8': {'>': '9', 'v': '5', '<': '7'},
    '9': {'v': '6', '<': '8'},
}
key_pad2 = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['X', '0', 'A'],
]
direction_pad = {
    ('A','A'): '',
    ('A','^'): '<',
    ('A','>'): 'v',
    ('A','v'): 'v<',
    ('A','<'): 'v<<',

    ('^','A'): '>',
    ('^','^'): '',
    ('^','>'): 'v>',
    ('^','v'): 'v',
    ('^','<'): 'v<',

    ('>','A'): '^',
    ('>','^'): '<^',
    ('>','>'): '',
    ('>','v'): '<',
    ('>','<'): '<<',

    ('v','A'): '^>',
    ('v','^'): '^',
    ('v','>'): '>',
    ('v','v'): '',
    ('v','<'): '<',

    ('<','A'): '>>^',
    ('<','^'): '>^',
    ('<','v'): '>',
    ('<','>'): '>>',
    ('<','<'): '',
}

@timeit
def calculate_score_pt1(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    for code in file:
        code = code.strip()
        cur_char = 'A'
        path1 = ''
        for char in code:
            while True:
                if cur_char == char:
                    path1 += 'A'
                    break
                options = key_pad[cur_char]
                if cur_char == 'A':
                    if char == '0':
                        path1 += '<'
                        cur_char = options['<']
                    else:
                        path1 += '^'
                        cur_char = options['^']
                else:
                    if char == 'A':
                        val = -1
                    else:
                        val = int(char)

                    lowest = (None, 1000)
                    for direction in DIRECTIONS:
                        dir_val = options.get(direction, 1000)
                        if dir_val == 'A':
                            if char == 'A':
                                lowest = direction, 0
                            continue
                        else:
                            dir_val = int(dir_val)
                            delta = abs(val - dir_val)
                            if delta < lowest[1]:
                                lowest = direction, delta
                    path1 += lowest[0]
                    cur_char = options[lowest[0]]

        path2 = ''
        cur_char = 'A'
        for char in path1:
            path2 += direction_pad[(cur_char, char)]
            path2 += 'A'
            cur_char = char

        path3 = ''
        cur_char = 'A'
        for char in path2:
            path3 += direction_pad[(cur_char, char)]
            path3 += 'A'
            cur_char = char

        print(path3, len(path3))
        print(path2)
        print(path1)
        print(code)

    return 0


@timeit
def calculate_score_pt2(test: bool) -> (int, int):
    return 0

if __name__ == '__main__':
    score = calculate_score_pt1(test=True)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=True)
    print(f'Score: {score}')