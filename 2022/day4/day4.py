from util.util import timeit

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("input_test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        pairs = line.split(",")
        l_range = pairs[0].split("-")
        r_range = pairs[1].split("-")

        l_range = [int(num) for num in l_range]
        r_range = [int(num) for num in r_range]

        if l_range[0] <= r_range[0] and l_range[1] >= r_range[1]:
            score += 1
        elif l_range[0] >= r_range[0] and l_range[1] <= r_range[1]:
            score += 1

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("input_test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        pairs = line.split(",")
        l_range = pairs[0].split("-")
        r_range = pairs[1].split("-")

        l_range = [int(num) for num in l_range]
        r_range = [int(num) for num in r_range]

        if l_range[0] <= r_range[1] and l_range[1] >= r_range[0]:
            score += 1
        elif r_range[0] <= l_range[1] and r_range[1] >= l_range[0]:
            score += 1

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
