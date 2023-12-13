from functools import cache
from util.util import timeit

test_data = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]


@cache
def find_valid_permutations(springs, groupings, groups_count=0):
    if springs == '':
        return groupings == () and groups_count == 0

    permutations = 0
    # Recursively branch if next letter is a '?'
    if springs[0] == "?":
        next_char = ['.', '#']
    else:
        next_char = springs[0]

    for char in next_char:
        if char == "#":
            permutations += find_valid_permutations(springs[1:], groupings, groups_count + 1)
        else:
            if groups_count:
                # End of group
                if groupings and groupings[0] == groups_count:
                    permutations += find_valid_permutations(springs[1:], groupings[1:])
            else:
                # Next char
                permutations += find_valid_permutations(springs[1:], groupings)
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

    score = 0

    for row, line in enumerate(spring_map):
        line_split = line.split()
        springs = line_split[0]
        groupings = [int(x) for x in line_split[1].split(',')]

        # Unfold
        springs = '?'.join([springs] * 5) + '.'  # Extra . at the end is easier than handling edge-cases
        groupings = groupings * 5

        score += find_valid_permutations(springs, tuple(groupings))
        # print(f'{row}: {line}')

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
