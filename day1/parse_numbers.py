number_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def reverse_array_vals(array):
    new_array = []
    for key, value in enumerate(array):
        new_array.append(value[::-1])

    return new_array


def find_numbers(line_str: str, reverse: bool = False) -> str:
    line_str_copy = line_str
    number_str_copy = number_str.copy()

    if reverse:
        line_str_copy = line_str_copy[::-1]
        number_str_copy = reverse_array_vals(number_str_copy)

    for idx, char in enumerate(line_str_copy):
        if char.isnumeric():
            return char
        for key, value in enumerate(number_str_copy, start=1):
            try:
                found_idx = line_str_copy.index(value)
            except ValueError:
                continue
            if idx == found_idx:
                return str(key)


if __name__ == '__main__':
    file = open("input.txt", "r")
    total = 0
    for line in file:
        orig_line = line
        first = find_numbers(line)
        last = find_numbers(line, reverse=True)
        print(f"{orig_line} --> {first}{last}")

        total += int(first + last)
    file.close()

    print(f"Total: {total}")
