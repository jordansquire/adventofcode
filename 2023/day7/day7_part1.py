import pandas as pd
from util.util import timeit

test_data = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483',
]

hand_type = {
    'FiveOfAKind': 1,
    'FourOfAKind': 2,
    'FullHouse': 3,
    'ThreeOfAKind': 4,
    'TwoPair': 5,
    'OnePair': 6,
    'HighCard': 7
}

card_rank = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def categorize_cards(cards) -> int:
    duplicate_map = {
        5: [],
        4: [],
        3: [],
        2: [],
        1: [],
    }
    for char in cards:
        repeat = cards.count(char)
        duplicate_map[repeat].append(char)

    if len(duplicate_map[5]):
        return hand_type['FiveOfAKind']
    if len(duplicate_map[4]):
        return hand_type['FourOfAKind']
    if len(duplicate_map[3]) and len(duplicate_map[2]):
        return hand_type['FullHouse']
    if len(duplicate_map[3]):
        return hand_type['ThreeOfAKind']
    if len(duplicate_map[2]) > 2:
        return hand_type['TwoPair']
    if len(duplicate_map[2]):
        return hand_type['OnePair']
    return hand_type['HighCard']


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    score = 0
    card_set = []
    for line in file:
        line_split = line.split()
        cards = line_split[0]

        card_set.append(
            {
                'cards': cards,
                'bid': int(line_split[1]),
                'hand_type': categorize_cards(cards),
                'rank': 0,
                'card1': cards[0],
                'card2': cards[1],
                'card3': cards[2],
                'card4': cards[3],
                'card5': cards[4],
            }
        )

    df = pd.DataFrame(card_set)

    df['card1'] = pd.Categorical(df['card1'], card_rank)
    df['card2'] = pd.Categorical(df['card2'], card_rank)
    df['card3'] = pd.Categorical(df['card3'], card_rank)
    df['card4'] = pd.Categorical(df['card4'], card_rank)
    df['card5'] = pd.Categorical(df['card5'], card_rank)

    df = df.sort_values(['hand_type', 'card1', 'card2', 'card3', 'card4', 'card5'])
    df = df.reset_index(drop=True)

    for index, row in df.iterrows():
        # print(f"cards: {row['cards']}, rank: {len(card_set) - index}, {len(card_set)}, {index}")
        score += row['bid'] * (len(card_set) - index)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(df)

    if not test:
        file.close()

    return score


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')