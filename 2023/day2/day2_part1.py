import re

test_data = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]


def get_id(sub_line:str) -> int:
    return int(re.search(r'\d+', sub_line).group())


def check_games(max_red, max_blue, max_green) -> int:
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
        game_id = get_id(game_split[0])

        round_split = game_split[1].split(';')

        for rounds in round_split:
            color_split = rounds.split(',')

            for color in color_split:
                color_count = color.strip().split()

                if max_list[color_count[1]] < int(color_count[0]):
                    max_list[color_count[1]] = int(color_count[0])

        if max_list['red'] <= max_red and max_list['green'] <= max_green and max_list['blue'] <= max_blue:
            total += game_id

    file.close()
    return total


if __name__ == '__main__':
    valid_games_total = check_games(max_red=12, max_green=13, max_blue=14)
    print(f'Total: {valid_games_total}')

