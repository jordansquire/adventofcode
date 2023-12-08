from math import lcm
from util.util import timeit

test_data = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)',
]


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    directions = []
    instruction_set = {}
    current_spots = []
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
        location = line_split[0].strip()
        instruction_set[location] = {
            'L': direction_split[0].replace('(', '').strip(),
            'R': direction_split[1].replace(')', '').strip(),
        }
        if location[2] == 'A':
            current_spots.append(location)

    if not test:
        file.close()

    print(directions)
    print(current_spots)
    # print(instruction_set)

    z_cadence = []
    for i in range(0, len(current_spots)):
        score = 0
        index = 0
        while True:
            current_spots[i] = instruction_set[current_spots[i]][directions[index]]
            score += 1
            if current_spots[i][2] == 'Z':
                z_cadence.append(score)
                break

            index += 1
            if index == len(directions):
                index = 0

    print(f'All paths z-cadence: {z_cadence}')

    return lcm(*z_cadence)


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')