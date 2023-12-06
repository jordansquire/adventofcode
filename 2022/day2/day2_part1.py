test_data = [
    'A Y',
    'B X',
    'C Z',
]


def score_round(opponent, mine):
    if mine == 'X' and opponent == 'A':
        return 1 + 3
    if mine == 'X' and opponent == 'B':
        return 1
    if mine == 'X' and opponent == 'C':
        return 1 + 6
    if mine == 'Y' and opponent == 'A':
        return 2 + 6
    if mine == 'Y' and opponent == 'B':
        return 2 + 3
    if mine == 'Y' and opponent == 'C':
        return 2
    if mine == 'Z' and opponent == 'A':
        return 3
    if mine == 'Z' and opponent == 'B':
        return 3 + 6
    if mine == 'Z' and opponent == 'C':
        return 3 + 3


def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        round = line.split()
        score += score_round(round[0], round[1])

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')