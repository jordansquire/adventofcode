test_data = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]


def find_number(line, col) -> str:
    if col >= len(line):
        return ''

    if line[col].isdigit():
        return line[col] + find_number(line, col+1)

    return ''


def symbol_check(schematic, row, col):
    if 0 <= row < len(schematic):
        if 0 <= col < len(schematic[row]):
            char = schematic[row][col]
            if char == '*':
                return [row, col]

    return None


def check_neighbors(schematic, start_row, start_col, num_str):
    for col in range(start_col - 1, start_col + len(num_str) + 1):
        # Check row above, middle, below
        for row in range(start_row - 1, start_row + 2):
            result = symbol_check(schematic, row, col)
            if result is not None:
                return result

    return None


def check_parts() -> int:
    file = open("input.txt", "r")
    # file = test_data
    total = 0
    schematic = []
    possible_gears = []
    for line in file:
        schematic.append(line)

    for row, line in enumerate(schematic):
        for col, char in enumerate(line):
            if not char.isdigit() or (col > 0 and line[col-1].isdigit()):
                continue

            number = find_number(line, col)
            result = check_neighbors(schematic, row, col, number)
            if result is not None:
                # print(f'{number} {result}')
                possible_gears.append([number, result])

    for index, gear in enumerate(possible_gears):
        for other_gear in range(index+1, len(possible_gears)):
            if gear[1][0] == possible_gears[other_gear][1][0] and gear[1][1] == possible_gears[other_gear][1][1]:
                total += int(gear[0]) * int(possible_gears[other_gear][0])

    file.close()
    # print(possible_gears)
    return total


if __name__ == '__main__':
    valid_parts_total = check_parts()
    print(f'Total: {valid_parts_total}')
