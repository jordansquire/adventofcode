from itertools import combinations
from util.util import timeit


@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
    else:
        file = open("input.txt", "r")


    # networks = []
    # for line in file:
    #     found = False
    #     line_split = line.strip().split('-')
    #     for network in networks:
    #         if line_split[0] in network:
    #             if line_split[1] not in network:
    #                 network.append(line_split[1])
    #             found = True
    #         elif line_split[1] in network:
    #             if line_split[0] not in network:
    #                 network.append(line_split[0])
    #             found = True
    #
    #     if not found:
    #         temp = [line_split[0], line_split[1]]
    #         networks.append(temp)

    pairs = []
    connections = {}
    for line in file:
        node1, node2 = line.strip().split('-')
        pairs.append((node1, node2))

        if node1 not in connections:
            connections[node1] = [node2]
        else:
            connections[node1].append(node2)

        if node2 not in connections:
            connections[node2] = [node1]
        else:
            connections[node2].append(node1)

    total = 0
    doubles = 0
    triples = 0
    for c in connections.keys():
        if c[0] != 't':
            continue
        for c1, c2 in combinations(connections[c], 2):
            if c1 in connections[c2]:
                if c1[0] == 't':
                    if c2[0] == 't':
                        triples += 1
                    else:
                        doubles += 1
                else:
                    if c2[0] == 't':
                        doubles += 1
                total += 1
    return total - doubles // 2 - 2 * triples // 3

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