from re import split

from util.util import timeit

test_data1 = [
    '47|53',
    '97|13',
    '97|61',
    '97|47',
    '75|29',
    '61|13',
    '75|53',
    '29|13',
    '97|29',
    '53|29',
    '61|53',
    '97|53',
    '61|29',
    '47|13',
    '75|47',
    '97|75',
    '47|61',
    '75|61',
    '47|29',
    '75|13',
    '53|13',
    '',
    '75,47,61,53,29',
    '97,61,53,29,13',
    '75,29,13',
    '75,97,47,61,53',
    '61,13,29',
    '97,13,75,29,47',
]


@timeit
def calculate_score_pt1(test: bool) -> int:
    if test:
        file = test_data1
    else:
        file = open("input.txt", "r")

    rules = {}
    score = 0
    for line in file:
        if '|' in line:
            x = line.split('|')
            key = int(x[0])
            if key in rules:
                rules[key].append(int(x[1]))
            else:
                rules[key] = [int(x[1])]

        if ',' in line:
            invalid = False
            pages = line.split(',')
            pages = [int(page) for page in pages]
            for i, page in enumerate(pages):
                if page in rules:
                    for rule in rules[page]:
                        # Check for rule violation in prior pages
                        if rule in pages[0:i]:
                            invalid = True
                            break

            if not invalid:
                score += pages[int(len(pages) / 2)]

    return score

@timeit
def calculate_score_pt2(test: bool) -> int:
    if test:
        file = test_data1
    else:
        file = open("input.txt", "r")

    rules = {}
    score = 0
    for line in file:
        if '|' in line:
            x = line.split('|')
            key = int(x[0])
            if key in rules:
                rules[key].append(int(x[1]))
            else:
                rules[key] = [int(x[1])]

        if ',' in line:
            invalid = True
            change = False
            pages = line.split(',')
            pages = [int(page) for page in pages]

            # Keep looping until there are no more changes required
            while invalid:
                updated = False
                for i, page in enumerate(pages):
                    if page in rules:
                        for rule in rules[page]:
                            if rule in pages[0:i]:
                                # If there is a rule violation, move the page right in front of the rule
                                pages.remove(page)
                                idx = pages.index(rule)
                                pages.insert(idx, page)
                                updated = True
                                break
                        # If we updated something we need to restart our rule evaluation
                        if updated:
                            change = True
                            break
                # If we made it through all loops without a change we are now valid
                if not updated:
                    invalid = False

            if change:
                score += pages[int(len(pages) / 2)]

    return score

if __name__ == '__main__':
    score = calculate_score_pt1(test=False)
    print(f'Score: {score}')

    score = calculate_score_pt2(test=False)
    print(f'Score: {score}')
