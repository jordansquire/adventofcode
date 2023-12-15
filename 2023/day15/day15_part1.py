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

    for step in steps:
        score += custom_hash(step)

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
