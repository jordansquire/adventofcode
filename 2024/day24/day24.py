from util.util import timeit

wires = {}


def _operate(a, operand, b, output):
    global wires
    if a not in wires or b not in wires:
        return a, operand, b, output

    if operand == 'AND':
        wires[output] = wires[a] and wires[b]
    if operand == 'OR':
        wires[output] = wires[a] or wires[b]
    if operand == 'XOR':
        wires[output] = wires[a] ^ wires[b]

    return None


@timeit
def calculate_score_pt1(test: bool) -> int:
    global wires
    if test:
        file = open("test2.txt", "r")
    else:
        file = open("input.txt", "r")

    for line in file:
        line_split = line.strip().split(':')
        if line_split[0] == '':
            break
        wires[line_split[0]] = bool(int(line_split[1]))

    later = []
    for line in file:
        line_split = line.strip().split('->')
        output = line_split[1].strip()
        a, operand, b  = line_split[0].strip().split()

        l = _operate(a, operand, b, output)
        if l is not None:
            later.append(l)

    while later:
        a, operand, b, output = later.pop(0)
        l = _operate(a, operand, b, output)
        if l is not None:
            later.append(l)

    binary_str = ''
    for wire in sorted(wires.keys()):
        if wire[0] == 'z':
            binary_str = str(int(wires[wire])) + binary_str
            print(wire, int(wires[wire]))

    print(binary_str)
    return int(binary_str, base=2)

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    return 0

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=True)
    print(f'Score: {score}')