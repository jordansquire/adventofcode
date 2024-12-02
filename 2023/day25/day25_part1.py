from util.util import timeit

test_data = [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr',
]
graph = {}


def find_all_paths(g, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in g:
        return []
    paths = []
    for node in g[start]:
        if node not in path:
            newpaths = find_all_paths(g, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    for y, line in enumerate(file):
        line_split = line.split(':')
        node = line_split[0]
        edges = line_split[1].split()
        graph[node] = edges
        for n in edges:
            if n in graph:
                graph[n].append(node)
            else:
                graph[n] = [node]

    if not test:
        file.close()

    score = 0
    x = find_all_paths(graph, node, edges[0])
    return score


if __name__ == '__main__':
    score = calculate_score(test=True)
    print(f'Score: {score}')
