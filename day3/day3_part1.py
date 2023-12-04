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
            if not char.isnumeric() and (char != '.' and char != '\n'):
                return True

    return False


def check_neighbors(schematic, start_row, start_col, num_str) -> bool:
    for col in range(start_col - 1, start_col + len(num_str) + 1):
        # Check row above, middle, below
        for row in range(start_row - 1, start_row + 2):
            if symbol_check(schematic, row, col):
                return True

    return False


def check_parts() -> int:
    file = open("input.txt", "r")
    # file = test_data
    total = 0
    schematic = []
    for line in file:
        schematic.append(line)

    for row, line in enumerate(schematic):
        for col, char in enumerate(line):
            if not char.isdigit() or (col > 0 and line[col-1].isdigit()):
                continue

            number = find_number(line, col)
            if check_neighbors(schematic, row, col, number):
                # print(f'{number}')
                total += int(number)

    file.close()
    return total


if __name__ == '__main__':
    valid_parts_total = check_parts()
    print(f'Total: {valid_parts_total}')
