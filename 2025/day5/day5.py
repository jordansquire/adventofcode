from util.util import timeit


@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    ranges = []
    ingredients = []
    line_break = 0
    for i, line in enumerate(file):
        if line_break == 0:
            if line == "\n":
                line_break = i
            else:
                r = line.strip().split("-")
                ranges.append((int(r[0]), int(r[1])))
        else:
            ingredients.append(int(line.strip()))

    score = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                score += 1
                break

    return score


def check_overlap(start1, end1, start2, end2):
    """
    Check if two number ranges overlap and return the merged range if so
    """
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)
    if overlap_start <= overlap_end:
        return min(start1, start2), max(end1, end2)
    else:
        return None, None


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    ranges = []
    ingredients = []
    line_break = 0
    for i, line in enumerate(file):
        if line_break == 0:
            if line == "\n":
                line_break = i
            else:
                r = line.strip().split("-")
                ranges.append((int(r[0]), int(r[1])))
        else:
            ingredients.append(int(line.strip()))

    while True:
        ranges_to_pop = []
        new_ranges = []
        for i, range1 in enumerate(ranges):
            for j in range(i, len(ranges)):
                # Skip checking this loop if there are pending updates
                if i == j or i in ranges_to_pop or j in ranges_to_pop:
                    continue

                range2 = ranges[j]
                new_range = check_overlap(range1[0], range1[1], range2[0], range2[1])
                if new_range != (None, None):
                    ranges_to_pop += [i,j]
                    new_ranges.append(new_range)

        ranges_to_pop = sorted(ranges_to_pop, reverse=True)
        if new_ranges:
            for r in ranges_to_pop:
                # Remove ranges that have been merged
                ranges.pop(r)

            for r in new_ranges:
                # Append the new ranges
                ranges.append(r)
        else:
            break

    score = 0
    for r in ranges:
        score += r[1] - r[0] + 1
    return score



if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 3
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 14
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')