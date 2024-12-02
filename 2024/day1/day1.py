from collections import Counter

from util.util import timeit

test_data = [
    '3   4',
    '4   3',
    '2   5',
    '1   3',
    '3   9',
    '3   3',
]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    a = []
    b = []
    for line in file:
        line_split = line.split()
        a.append(int(line_split[0]))
        b.append(int(line_split[1]))

    a.sort()
    b.sort()

    score = 0
    for i in range(len(a)):
        score += abs(a[i] - b[i])

    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    a = []
    b = []
    for line in file:
        line_split = line.split()
        a.append(int(line_split[0]))
        b.append(int(line_split[1]))

    a_ct = Counter(a)
    b_ct = Counter(b)

    score = 0

    for key in a_ct:
        score += key * a_ct[key] * b_ct[key]

    return score

if __name__ == '__main__':
    # score = calculate_score_pt1(test=False)
    # print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')