from util.util import timeit

test_data = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#',
]


def validate_reflection(mirror, index, next_index, differences):
    if index == -1 or next_index == len(mirror):
        return differences == 1
    if mirror[index] == mirror[next_index]:
        return validate_reflection(mirror, index-1, next_index+1, differences)
    if sum(1 for a, b in zip(mirror[index], mirror[next_index]) if a != b) == 1:
        return validate_reflection(mirror, index-1, next_index+1, differences+1)
    else:
        return False


def find_reflection(mirrors, transpose=False):
    mirror = mirrors.copy()
    if transpose:
        mirror = [''.join(s) for s in zip(*mirror)]

    mirror_location = 0
    for index in range(0, len(mirror)):
        next_index = index + 1
        if next_index == len(mirror):
            break
        if validate_reflection(mirror, index, next_index, 0):
            mirror_location = index + 1
            break

    if mirror_location:
        # print(f'Reflection: {mirror_location}, Transpose: {transpose}')
        if transpose:
            return mirror_location
        else:
            return mirror_location * 100
    else:
        if transpose:
            return 0
        return find_reflection(mirror, transpose=True)


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    mirror_maps = []
    mirrors = []
    for line in file:
        line = line.strip()
        if line == '':
            mirror_maps.append(mirrors)
            mirrors = []
        else:
            mirrors.append(line)
    mirror_maps.append(mirrors)

    if not test:
        file.close()

    score = 0
    for mirrors in mirror_maps:
        score += find_reflection(mirrors)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
