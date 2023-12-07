test_data = [
    'A Y',
    'B X',
    'C Z',
]

# (1 for Rock, 2 for Paper, and 3 for Scissors)
# (0 if you lost, 3 if the round was a draw, and 6 if you won).
score_map = {
    'AX': 3 + 0,  # rock, lose (scissors)
    'AY': 1 + 3,  # rock, draw (rock)
    'AZ': 2 + 6,  # rock, win (paper)
    'BX': 1 + 0,  # paper, lose (rock)
    'BY': 2 + 3,  # paper, draw (paper)
    'BZ': 3 + 6,  # paper, win (scissors)
    'CX': 2 + 0,  # scissors, lose (paper)
    'CY': 3 + 3,  # scissors, draw (scissors)
    'CZ': 1 + 6,  # scissors, win (rock)
}


def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        round = line.split()
        score += score_map[round[0] + round[1]]

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')