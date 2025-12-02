from util.util import timeit


def _try_key_in_lock(key: [], lock: []) -> bool:
    for l, k in zip(lock, key):
        if l + k > 5:
            return False
    return True


@timeit
def calculate_score_pt1(test: bool) -> int:
    global wires
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    locks = []
    keys = []
    temp = []
    for line in file:
        line = line.strip()
        if line.strip() == '':
            # Transpose for convenience
            transposed = list(zip(*temp))
            device = [x.count('#') - 1 for x in transposed]

            if temp[0].count('#') > 0:
                locks.append(device)
            else:
                keys.append(device)
            temp = []
            continue

        temp.append([c for c in line])

    score = 0
    for key in keys:
        for lock in locks:
            if _try_key_in_lock(key, lock):
                score += 1

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    return 0

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=True)
    print(f'Score: {score}')