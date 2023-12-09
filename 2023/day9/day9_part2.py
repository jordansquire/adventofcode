from util.util import timeit

test_data = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45',
]


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    for line in file:
        nums = line.split()
        sequences = {}
        sequence = []
        for num in nums:
            sequence.append(int(num))

        end = False
        last_index = 0
        max_index = len(sequence)
        sequences[len(sequence)] = sequence
        while True:
            cur_sequence = sequence

            end = True
            sequence = []
            for idx in range(0, len(cur_sequence) - 1):
                diff = int(cur_sequence[idx+1]) - int(cur_sequence[idx])
                sequence.append(diff)
                end &= diff == 0

            sequences[len(sequence)] = sequence
            last_index = len(sequence)

            if end:
                break

        last_val = 0
        for idx in range(last_index, max_index+1):
            sequence = sequences[idx]
            if idx == last_index:
                sequence.append(0)
                continue

            sequence.append(sequence[0] - last_val)
            last_val = sequence[len(sequence)-1]

        score += last_val
        # print(sequences)

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=True)
    print(f'Score: {score}')
