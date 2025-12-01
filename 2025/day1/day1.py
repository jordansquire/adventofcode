from collections import Counter

from util.util import timeit

test_data = [
    'L68',
    'L30',
    'R48',
    'L5',
    'R60',
    'L55',
    'L1',
    'L99',
    'R14',
    'L82',
]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    direction = []
    count = []
    for line in file:
        direction.append(line[0])
        count.append(int(line[1:].strip()))

    score = 0
    dial = 50

    for i in range(0, len(direction)):
        x = count[i] % 100
        if direction[i] == 'L':
            dial -= x
        else:
            dial += x

        if dial < 0:
            dial += 100

        if dial > 99:
            dial -= 100

        # print(f'dial is rotated {direction[i]}{count[i]} to {dial}')
        score += (dial == 0)

    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    direction = []
    count = []
    for line in file:
        direction.append(line[0])
        count.append(int(line[1:].strip()))

    score = 0
    dial = 50

    for i in range(0, len(direction)):
        past = (dial == 0)
        new_dial = count[i] % 100
        score += int(count[i] / 100)

        if direction[i] == 'L':
            dial -= new_dial
        else:
            dial += new_dial

        if dial < 0:
            dial += 100
            if not past:
                score += 1

        elif dial > 99:
            dial -= 100
            if not past:
                score += 1

        elif dial == 0 :
            score += 1

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')