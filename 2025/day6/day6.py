from util.util import timeit


@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    problems = []
    operations = []
    for i, line in enumerate(file):
        if line[0] == '*' or line[0] == '+':
            operations = [o for o in line.split() if o.isascii()]
        else:
            problems.append([s for s in line.split() if s.isdigit()])

    score = []
    for col in range(len(problems[0])):
        vals = []
        for row in range(len(problems)):
            vals.append(problems[row][col])
        op = operations[col].join(vals)
        score.append(eval(op))
    return sum(score)


@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    lines = []
    problems = []
    score = []
    max_len = 0
    for line in file:
        lines.append(line)
        max_len = max(max_len, len(line))

    # Iterate over each column of characters, starting at the end of the string
    for col in range(max_len - 2, -1, -1):
        digits = []
        # Iterate over each row and extract the digit if it exists
        for row in range(len(lines) - 1):
            if len(lines[row]) > col:
                l = lines[row][col]
                if l != ' ':
                    digits.append(l)

        # Attempt to form a number out of the digits
        number = "".join(digits)
        if number.strip() != '':
            problems.append(number)

        # If there is an operator in the last row we are redy to evaluate the operation
        if len(lines[len(lines)-1]) > col:
            operator = lines[len(lines)-1][col]
            if operator.strip() != '':
                op = operator.join(problems)
                score.append(eval(op))
                problems.clear()

    return sum(score)



if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 4277556
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 3263827
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')