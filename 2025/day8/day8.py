from util.util import timeit
import math

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points
    """
    sq_diff = 0
    for i in range(len(point1)):
        sq_diff += (point1[i] - point2[i]) ** 2
    return math.sqrt(sq_diff)

def consolidate_circuits(circuits):
    """
    Consolidate circuits that overlap
    """
    for i in range(len(circuits)):
        for j in range(i + 1, len(circuits)):
            if circuits[j] & circuits[i]:
                circuits[j] |= circuits[i]
                circuits[i] = None
                break
    return [item for item in circuits if item is not None]

@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
        num_connections = 10
    else:
        file = open("input.txt", "r")
        num_connections = 1000

    points = []
    for line in file:
        pts = line.strip().split(',')
        x = int(pts[0])
        y = int(pts[1])
        z = int(pts[2])
        points.append((x, y, z))

    # Find the distance between all points
    distances = []
    for i, pt1 in enumerate(points):
        for j in range(i+1, len(points)):
            pt2 = points[j]
            dist = euclidean_distance(pt1, pt2)
            distances.append({'pt1':i, 'pt2':j, 'dist':dist})

    sorted_distances = sorted(distances, key=lambda x: x["dist"])

    # Join the closest [num_connections] points by shortest distance
    circuits = []
    for i in range(num_connections):
        pt1 = points[sorted_distances[i]['pt1']]
        pt2 = points[sorted_distances[i]['pt2']]

        for circuit in circuits:
            if pt1 in circuit and pt2 in circuit:
                break
            elif pt1 in circuit:
                circuit.add(pt2)
                break
            elif pt2 in circuit:
                circuit.add(pt1)
                break

        circuits.append({pt1, pt2})
        circuits = consolidate_circuits(circuits)

    sizes = [len(circuit) for circuit in circuits if circuit is not None]
    sizes.sort(reverse=True)

    return sizes[0] * sizes[1] * sizes[2]

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = open("test.txt", "r")
        num_connections = 10
    else:
        file = open("input.txt", "r")
        num_connections = 1000

    points = []
    for line in file:
        pts = line.strip().split(',')
        x = int(pts[0])
        y = int(pts[1])
        z = int(pts[2])
        points.append((x, y, z))

    # Find the distance between all points
    distances = []
    for i, pt1 in enumerate(points):
        for j in range(i + 1, len(points)):
            pt2 = points[j]
            dist = euclidean_distance(pt1, pt2)
            distances.append({'pt1': i, 'pt2': j, 'dist': dist})

    sorted_distances = sorted(distances, key=lambda x: x["dist"])

    # Join all points starting at the nearest ones until all points have been connected
    circuits = []
    for i in range(len(sorted_distances)):
        pt1 = points[sorted_distances[i]['pt1']]
        pt2 = points[sorted_distances[i]['pt2']]

        for circuit in circuits:
            if pt1 in circuit and pt2 in circuit:
                break
            elif pt1 in circuit:
                circuit.add(pt2)
                break
            elif pt2 in circuit:
                circuit.add(pt1)
                break

        circuits.append({pt1, pt2})
        circuits = consolidate_circuits(circuits)

        # If all points are in the network we are done
        if len(circuits[0]) == len(points):
            return pt1[0] * pt2[0]

    return 0


if __name__ == '__main__':
    assert calculate_score_pt1(test=True) == 40
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    assert calculate_score_pt2(test=True) == 25272
    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')