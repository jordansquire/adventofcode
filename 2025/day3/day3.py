from util.util import timeit

test_data = [
    '987654321111111',
    '811111111111119',
    '234234234234278',
    '818181911112111',
]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        line = line.strip()
        max_digit_1 = 0
        max_location = 0
        for i, digit in enumerate(line):
            # The last digit can't be the right choice
            if i == len(line) - 1:
                continue

            if int(digit) > max_digit_1:
                max_digit_1 = int(digit)
                max_location = i

        max_digit_2 = 0
        for i in range(max_location + 1, len(line)):

            if int(line[i]) > max_digit_2:
                max_digit_2 = int(line[i])

        score += max_digit_1 * 10 + max_digit_2

    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        line = line.strip()

        batteries = []
        for j, digit_str in enumerate(line):
            digit = int(digit_str)

            # Prepopulate the first 12 digits
            if len(batteries) < 12:
                batteries.append(digit)
                continue

            # Starting with the left-most digit see if we can increase the
            # value by shifting the digits left
            for i, d in enumerate(batteries):
                # Handle last digit
                if i == len(batteries) - 1:
                    if digit > d:
                        batteries[i] = digit
                    break

                # If the digits can be shifted drop the low digit and append
                # the new digit to the right
                if d < batteries[i+1]:
                    batteries.pop(i)
                    batteries.append(digit)
                    break

        score += int("".join(map(str, batteries)))
    return score


if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 357
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 3121910778619
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')