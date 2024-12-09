from util.util import timeit

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    disk_map = []
    file_str = file.read()
    file_id = 0
    for i, char in enumerate(file_str):
        num = int(char)

        if i % 2:
            for j in range(num):
                disk_map.append(None)
        else:
            for j in range(num):
                disk_map.append(file_id)
            file_id += 1

    # Shuffle file pieces to the first open spot
    reverse_index = len(disk_map) - 1
    for index in range(len(disk_map)):
        while disk_map[reverse_index] is None:
            reverse_index -= 1

        if index >= reverse_index:
            break

        if disk_map[index] is not None:
            continue

        disk_map[index] = disk_map[reverse_index]
        disk_map[reverse_index] = None

    score = 0
    for i, block in enumerate(disk_map):
        if block is None:
            break
        score += block * i
    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")

    disk_map = []
    file_str = file.read()
    file_id = 0
    for i, char in enumerate(file_str):
        num = int(char)
        if num == 0:
            continue

        if i % 2:
            disk_map.append((None, num))
        else:
            disk_map.append((file_id, num))
            file_id += 1

    # Find the first contiguous big enough to fit the whole file
    reverse_index = len(disk_map) - 1
    while reverse_index > 0:
        file = disk_map[reverse_index]
        if file[0] is None:
            reverse_index -= 1
            continue

        for i, block in enumerate(disk_map):
            if i >= reverse_index:
                break

            if block[0] is None and block[1] >= file[1]:
                disk_map[i] = file
                if block[1] > file[1]:
                    disk_map.insert(i+1, (None, block[1] - file[1]))
                    reverse_index += 1
                disk_map[reverse_index] = (None, file[1])
                break
        reverse_index -= 1

    score = 0
    mem_map = []
    for block in disk_map:
        for i in range(block[1]):
            mem_map.append(block[0])

    for i, block in enumerate(mem_map):
        if block is None:
            continue
        score += block * i
    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
