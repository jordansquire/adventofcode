from functools import cache
from util.util import timeit

candidates = []
reject_list = {}


@cache
def _get_next_towels(partial: str, iter, solution: str, min_len: int, max_len: int) -> int:
    global reject_list
    if iter not in  reject_list:
        reject_list[iter] = set()

    start_index = len(partial)
    matches = set()
    for i in range(min_len, max_len + 1):
        matches = matches.union({c for c in candidates[iter] if c == solution[start_index:start_index + i]})

    score = 0
    for match in matches:
        new_partial = partial + match
        if new_partial == solution:
            score += 1
        if (partial, match) in reject_list[iter]:
            continue

        val = _get_next_towels(new_partial, iter, solution, min_len, max_len)
        if val:
            score += val
        else:
            reject_list[iter] = reject_list[iter].union({(partial, match)})

    return score


@timeit
def calculate_score(test: bool) -> (int, int):
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    towels = [x.strip() for x in file.readline().split(",")]
    file.readline()

    score_pt1 = score_pt2 = 0
    for i, line in enumerate(file):
        solution = line.strip()

        candidates.append({t for t in towels if t in solution})
        min_len = min([len(t) for t in candidates[i]])
        max_len = max([len(t) for t in candidates[i]])

        score = _get_next_towels('', i, solution, min_len, max_len)
        if score:
            score_pt1 += 1
            score_pt2 += score
        # print(f"Processing line {i}: {solution}, {score}")

    return score_pt1, score_pt2


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
