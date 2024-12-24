from util.util import timeit


def _mix(a:int, b:int) -> int:
    return a ^ b


def _prune(a:int) -> int:
    return a % 16777216


def _generate_secret_number(seed: int):
    num = _prune(_mix(seed * 64, seed))
    num = _prune(_mix(int(num / 32), num))
    num = _prune(_mix(num * 2048, num))
    return num



@timeit
def calculate_score_pt1(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        val = int(line)
        num = val
        for i in range(2000):
            num = _generate_secret_number(num)
        # print(f"{val}: {num}")
        score += num

    return score


@timeit
def calculate_score_pt2(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")


    all_deltas = []
    delta_set = {}
    for line in file:
        line_num = int(line)
        num = line_num
        seq = []
        for i in range(2000):
            next_num = _generate_secret_number(num)
            val = next_num % 10
            seq.append(val)
            num = next_num

        deltas = {}
        delta_seq = []
        prev_num = seq[0]
        for i in range(1, len(seq) - 1, 1):
            seq_val = seq[i]
            if len(delta_seq) < 3:
                delta_seq.append(seq_val - prev_num)
            else:
                delta_seq.append(seq_val - prev_num)
                new_seq = (delta_seq[0], delta_seq[1], delta_seq[2], delta_seq[3])
                if new_seq not in deltas.keys():
                    deltas[new_seq] = seq_val
                if new_seq not in all_deltas:
                    all_deltas.append(new_seq)
                delta_seq.pop(0)

            prev_num = seq_val

        delta_set[line_num] = dict(sorted(deltas.items(), key=lambda item: item[1], reverse=True))

    max_score = 0
    for d in all_deltas:
        score = 0
        for key in delta_set.keys():
            score += delta_set[key].get(d, 0)
        if score > max_score:
            print(d, score)
            max_score = score

    return max_score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')