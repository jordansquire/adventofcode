from util.util import timeit

test_data1 = [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)',
]

test_data2 = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)',
]


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data2
    else:
        file = open("input.txt", "r")

    score = 0
    directions = []
    instruction_set = {}
    first = True
    for line in file:
        if first:
            directions = line.strip()
            first = False
            continue

        if line.strip() == "":
            continue

        line_split = line.split("=")
        direction_split = line_split[1].split(',')
        instruction_set[line_split[0].strip()] = {
            'L': direction_split[0].replace('(', '').strip(),
            'R': direction_split[1].replace(')', '').strip(),
        }

    print(directions)
    # print(instruction_set)

    current_spot = 'AAA'
    index = 0
    end_spot = 'ZZZ'
    while True:
        current_spot = instruction_set[current_spot][directions[index]]
        score += 1

        if current_spot == end_spot:
            break

        index += 1
        if index == len(directions):
            index = 0

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')