test_data = [
    'Time:      71530',
    'Distance:  940200',
]


def num_winners(time, distance_record, speed) -> int:
    winners = 0
    distance = speed * (time - speed)
    while distance > distance_record and speed > 0:
        winners += 1
        speed -= 1
        distance = speed * (time - speed)

    return winners


def calculate_score(test: bool) -> int:
    if test:
        file = test_data
        times = file[0].split()
        distances = file[1].split()
    else:
        file = open("input2.txt", "r")
        times = file.readline().split()
        distances = file.readline().split()

    score = 0

    for race in range(1, len(times)):
        time = int(times[race])
        distance_record = int(distances[race])
        winners = num_winners(time, distance_record, int(time/2)) * 2
        if time % 2 == 0:
            winners -= 1

        print(f'Time: {time} Record: {distance_record} Winners: {winners}')

        if score == 0:
            score = winners
        else:
            score *= winners

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
