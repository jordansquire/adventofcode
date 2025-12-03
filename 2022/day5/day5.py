from util.util import timeit

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    box_lines = []
    instructions = []
    line_break = 0
    for i, line in enumerate(file):
        if line_break == 0:
            if line == "\n":
                line_break = i
            else:
                box_lines.append(line)
        else:
            instructions.append(line)

    column_count = int(box_lines[-1].strip()[-1])
    box_lines.pop()

    # Create stacks
    stacks = []
    for column in range(column_count):
        boxes = []
        for line in box_lines:
            idx = column*4 + 1
            if idx < len(line):
                if line[idx].strip() != '':
                    boxes.append(line[idx])
        boxes.reverse()
        stacks.append(boxes)

    # Execute instructions
    for inst in instructions:
        extraction = [int(s) for s in inst.split() if s.isdigit()]
        num_boxes, from_stack, to_stack = extraction[0], extraction[1], extraction[2]
        for _ in range(num_boxes):
            stacks[to_stack-1].append(stacks[from_stack-1].pop())

    # Generate message
    message = ''
    for stack in stacks:
        message += stack.pop()
    return message

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    box_lines = []
    instructions = []
    line_break = 0
    for i, line in enumerate(file):
        if line_break == 0:
            if line == "\n":
                line_break = i
            else:
                box_lines.append(line)
        else:
            instructions.append(line)

    column_count = int(box_lines[-1].strip()[-1])
    box_lines.pop()

    # Create stacks
    stacks = []
    for column in range(column_count):
        boxes = []
        for line in box_lines:
            idx = column * 4 + 1
            if idx < len(line):
                if line[idx].strip() != '':
                    boxes.append(line[idx])
        boxes.reverse()
        stacks.append(boxes)

    # Execute instructions
    for inst in instructions:
        extraction = [int(s) for s in inst.split() if s.isdigit()]
        num_boxes, from_stack, to_stack = extraction[0], extraction[1], extraction[2]
        movers = []
        for _ in range(num_boxes):
            movers.append(stacks[from_stack-1].pop())

        movers.reverse()
        stacks[to_stack - 1] += movers

    # Generate message
    message = ''
    for stack in stacks:
        message += stack.pop()
    return message

if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 'CMZ'
    message = calculate_score_pt1(test=False)
    print(f'Message: {message}')

    assert calculate_score_pt2(test=True) == 'MCD'
    message = calculate_score_pt2(test=False)
    print(f'Message: {message}')