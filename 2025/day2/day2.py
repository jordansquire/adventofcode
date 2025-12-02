from util.util import timeit

test_data = '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        data = test_data
    else:
        file = open("input.txt", "r")
        data = file.readline()

    score = 0
    ranges = data.split(',')

    for num_range in ranges:
        lower_str, upper_str = num_range.split('-')
        lower = int(lower_str)
        upper = int(upper_str)
        for num in range(lower, upper+1):
            num_str = str(num)
            if len(num_str) % 2 != 0:
                continue

            candidate = num_str[:int(len(num_str) / 2)] * 2
            if num_str == candidate:
                score += num
                # print(candidate)

    return score


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        data = test_data
    else:
        file = open("input.txt", "r")
        data = file.readline()

    score = 0
    ranges = data.split(',')

    for num_range in ranges:
        lower_str, upper_str = num_range.split('-')
        lower = int(lower_str)
        upper = int(upper_str)
        for num in range(lower, upper+1):
            num_str = str(num)
            for i in range(1, int(len(num_str) / 2) + 1):
                if len(num_str) % i != 0:
                    continue

                repeat_count = int(len(num_str) / i)
                candidate = num_str[:i] * repeat_count
                if num_str == candidate:
                    score += num
                    # print(candidate)
                    break

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')