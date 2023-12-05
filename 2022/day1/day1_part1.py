test_data = [
    '1000',
    '2000',
    '3000',
    '',
    '4000',
    '',
    '5000',
    '6000',
    '',
    '7000',
    '8000',
    '9000',
    '',
    '10000',
]


def check_calories() -> int:
    file = open("input.txt", "r")
    # file = test_data

    max_total = 0
    total = 0
    for line in file:
        if not line.strip().isnumeric():
            print(f'Non-numeric line ({line.strip()}), current total = {total}, max total = {max_total}')
            if max_total < total:
                max_total = total

            total = 0
            continue

        # print(f'Numeric line: {line.strip()}')
        total += int(line)

    file.close()
    return max_total


if __name__ == '__main__':
    max_calories = check_calories()
    print(f'Max total: {max_calories}')
