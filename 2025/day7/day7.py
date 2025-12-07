from util.util import timeit


@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    paths = set()
    score = 0
    for i, line in enumerate(file):
        cur_paths = set()
        if 'S' in line:
            cur_paths.add(line.index('S'))
        else:
            for x in paths:
                if line[x] == '^':
                    cur_paths.add(x - 1)
                    cur_paths.add(x + 1)
                    score += 1
                else:
                    cur_paths.add(x)

        paths = cur_paths.copy()

    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    beams = []
    for row, line in enumerate(file):
        line = line.strip()
        new_beams = [0] * (len(line))
        if row == 0:
            new_beams[line.index('S')] = 1

        else:
            for i, beam in enumerate(beams):
                if line[i] == '.':
                    new_beams[i] += beams[i]
                elif line[i] == '^':
                    new_beams[i-1] += beams[i]
                    new_beams[i+1] += beams[i]

        beams = new_beams.copy()

    return sum(beams)


if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 21
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 40
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')