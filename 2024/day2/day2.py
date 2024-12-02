from util.util import timeit

test_data = [
    '7 6 4 2 1',
    '1 2 7 8 9',
    '9 7 6 2 1',
    '1 3 2 4 5',
    '8 6 4 4 1',
    '1 3 6 7 9',
]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    reports = []
    for line in file:
        reports.append(list(map(int,line.split())))

    score = 0
    for levels in reports:
        deltas = []
        for i in range(len(levels) - 1):
            deltas.append(levels[i] - levels[i + 1])

        # Check that all values are increasing or decreasing
        if not(max(deltas) > 0 and min(deltas) > 0) and not(max(deltas) < 0 and min(deltas) < 0):
            continue  # Not safe

        # Check that all deltas are at most |3|
        if max(deltas) > 3 or min(deltas) < -3:
            continue  # Not safe

        score += 1  # Safe

    return score

def _generate_deltas(levels: list) -> list:
    # Generate the deltas between each level reading
    deltas = []
    for i in range(len(levels) - 1):
        deltas.append(levels[i] - levels[i + 1])
    return deltas

def _unsafe_index(deltas: list) -> int:
    # Find the index of any unsafe deltas
    positive = None
    for i, delta in enumerate(deltas):
        if positive is None:
            positive = delta > 0

        if delta == 0 or abs(delta) > 3:
            return i

        if (positive and delta < 0) or (not positive and delta > 0):
            return i
    return -1

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    reports = []
    for line in file:
        reports.append(list(map(int, line.split())))

    score = 0

    for levels in reports:
        if _unsafe_index(_generate_deltas(levels)) == -1:
            score += 1  # Safe
        else:
            # If the levels are unsafe, apply the dampener to attempt to find a safe configuration
            for i in range(len(levels)):
                dampener = levels.copy()
                dampener.pop(i)
                if _unsafe_index(_generate_deltas(dampener)) == -1:
                    score += 1
                    break

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')