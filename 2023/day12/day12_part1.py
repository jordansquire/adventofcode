import itertools
from util.util import timeit

test_data = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]


def is_valid_permutation(line, groupings) -> bool:
    expected_num_springs = sum(groupings)
    num_springs = line.count('#')
    if num_springs != expected_num_springs:
        return False

    line_groupings = []
    group_count = 0
    for char in line:
        if char == '#':
            group_count += 1
        if char == '.' and group_count > 0:
            line_groupings.append(group_count)
            group_count = 0

    if group_count > 0:
        line_groupings.append(group_count)

    return line_groupings == groupings


def get_wildcard_locations(line) -> []:
    wildcard_locations = []
    for index, char in enumerate(line):
        if char == '?':
            wildcard_locations.append(index)

    return wildcard_locations


def find_valid_permutations(line) -> int:
    permutations = 0

    line_split = line.split()
    springs = line_split[0]
    grouping_split = line_split[1].split(',')
    groupings = []
    for group in grouping_split:
        groupings.append(int(group))
    expected_num_springs = sum(groupings)
    num_springs = springs.count('#')
    wildcard_locations = get_wildcard_locations(springs)

    for spring_locations in itertools.combinations(wildcard_locations, expected_num_springs-num_springs):
        potential_springs = ""
        for index, char in enumerate(springs):
            if index in wildcard_locations:
                if index in spring_locations:
                    potential_springs += "#"
                else:
                    potential_springs += "."
            else:
                potential_springs += char
        permutations += is_valid_permutation(potential_springs, groupings)

    return permutations


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    spring_map = []
    for line in file:
        spring_map.append(line.strip())

    if not test:
        file.close()

    # print(spring_map)
    score = 0

    for line in spring_map:
        score += find_valid_permutations(line)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
