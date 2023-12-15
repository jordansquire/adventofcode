from util.util import timeit

test_data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'


def custom_hash(string) -> int:
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val = val % 256
    return val


@timeit
def calculate_score(test: bool) -> int:
    if test:
        sequence = test_data
    else:
        file = open("input.txt", "r")
        sequence = file.readline()

    steps = sequence.strip().split(',')

    if not test:
        file.close()

    score = 0
    boxes = {}

    for step in steps:
        if step.count('='):
            split_char = '='
        else:
            split_char = '-'

        step_split = step.split(split_char)
        label = step_split[0]
        box = custom_hash(label)

        if split_char == '=':
            focal_length = int(step_split[1])
            if box not in boxes.keys():
                boxes[box] = [{label: focal_length}]
            else:
                try:
                    box_index = next((i for i, item in enumerate(boxes[box]) if item[label]), None)
                    boxes[box][box_index] = {label: focal_length}
                except KeyError:
                    boxes[box].append({label: focal_length})

        else:
            try:
                box_index = next((i for i, item in enumerate(boxes[box]) if item[label]), None)
                if box_index:
                    boxes[box].pop(box_index)
            except KeyError:
                pass

    for box in boxes:
        for slot, lense in enumerate(boxes[box]):
            score += (box + 1) * (slot + 1) * next(iter(lense.values()))

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
