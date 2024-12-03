from util.util import timeit

test_data1 = [
    'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))',
]

test_data2 = [
    'xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))',
]

def try_cast_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data1
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        operations = line.split('mul(')
        for operation in operations:
            num1 = None
            num_str = ''
            for char in operation:
                # Handle comma
                if char == ',' and num_str != '' and num1 is None:
                    num1 = try_cast_to_int(num_str)
                    num_str = ''
                    continue

                # Operation parameters complete, update score
                if char == ')' and num1 is not None and num_str != '':
                    num2 = try_cast_to_int(num_str)
                    score += num1 * num2
                    break  # Operation complete

                digit = try_cast_to_int(char)

                if digit is not None:
                    num_str += char
                    continue

                break  # Invalid operation if we got this far

    return score

def _perform_operation(operation: str) -> int:
    num1 = None
    num_str = ''
    for char in operation:
        # Handle comma
        if char == ',' and num_str != '' and num1 is None:
            num1 = try_cast_to_int(num_str)
            num_str = ''
            continue

        # Operation parameters complete, update score
        if char == ')' and num1 is not None and num_str != '':
            num2 = try_cast_to_int(num_str)
            return num1 * num2  # Operation complete

        digit = try_cast_to_int(char)

        if digit is not None:
            num_str += char
            continue

        return 0  # Invalid operation if we got this far
    return 0  # Invalid operation if we got this far

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data2
    else:
        file = open("input.txt", "r")

    score = 0
    suppress = False
    for line in file:
        operations = line.split('mul(')
        for operation in operations:
            last_do_idx = operation.rfind('do()')
            last_dont_idx = operation.rfind("don't()")
            if last_do_idx > last_dont_idx:
                if not suppress:
                    score += _perform_operation(operation)
                suppress = False
            elif last_do_idx < last_dont_idx:
                if not suppress:
                    score += _perform_operation(operation)
                suppress = True
            else:
                if not suppress:
                    score += _perform_operation(operation)

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
