test_data = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]


def check_games() -> int:
    file = open("input.txt", "r")
    # file = test_data
    total = 0
    for line in file:
        max_list = {
            'red': 0,
            'blue': 0,
            'green': 0,
        }
        game_split = line.split(':')

        round_split = game_split[1].split(';')

        for rounds in round_split:
            color_split = rounds.split(',')

            for color in color_split:
                color_count = color.strip().split()

                if max_list[color_count[1]] < int(color_count[0]):
                    max_list[color_count[1]] = int(color_count[0])

        total += max_list['red'] * max_list['green'] * max_list['blue']

    file.close()
    return total


if __name__ == '__main__':
    games_power_total = check_games()
    print(f'Total: {games_power_total}')

