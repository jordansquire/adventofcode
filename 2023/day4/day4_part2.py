import re

test_data = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]


def score_card(cards, index):
    if index >= len(cards):
        return 0

    game_split = cards[index].split(':')
    number_sets = game_split[1].split('|')
    winning_numbers = number_sets[0].split()
    card_numbers = number_sets[1].split()

    count_winning_numbers = 0
    for num in card_numbers:
        if num in winning_numbers:
            count_winning_numbers += 1

    card_count = 0
    for copy in range(1, count_winning_numbers+1):
        card_count += score_card(cards, index+copy)

    return 1 + card_count


def check_cards() -> int:
    file = open("input.txt", "r")
    # file = test_data
    total = 0
    cards = []
    for line in file:
        cards.append(line)

    for index in range(0, len(cards)):
        total += score_card(cards, index)

    file.close()
    return total


if __name__ == '__main__':
    points_total = check_cards()
    print(f'Total: {points_total}')
