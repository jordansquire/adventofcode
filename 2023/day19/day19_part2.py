from copy import deepcopy
from util.util import timeit

test_data = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
]
rules = {}


def find_ranges(ranges, dest):
    if dest == 'A':
        a = len(ranges['x']) * len(ranges["m"]) * len(ranges["a"]) * len(ranges["s"])
        return a
    if dest == 'R':
        return 0
    rule_set = rules[dest]
    possibility_count = 0
    for rule in rule_set:
        if rule['key'] is not None:
            if rule['operation'] == '<':
                branch_true = range(ranges[rule['key']].start, rule['value'])
                branch_false = range(rule['value'], ranges[rule['key']].stop)
                range_true = deepcopy(ranges)
                range_true[rule['key']] = branch_true

                ranges[rule['key']] = branch_false

                possibility_count += find_ranges(range_true, rule['destination'])
            if rule['operation'] == '>':
                branch_true = range(rule['value'] + 1, ranges[rule['key']].stop)
                branch_false = range(ranges[rule['key']].start, int(rule['value']) + 1)
                range_true = deepcopy(ranges)
                range_true[rule['key']] = branch_true

                ranges[rule['key']] = branch_false

                possibility_count += find_ranges(range_true, rule['destination'])
        else:
            possibility_count += find_ranges(ranges, rule['destination'])

    return possibility_count


@timeit
def calculate_score(test: bool) -> int:
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    rules_parse = True
    for line in file:
        if line.strip() == '':
            rules_parse = False
            continue

        if rules_parse:
            line_split = line.strip().replace('}', '').split('{')
            rule_label = line_split[0]
            rule_split = line_split[1].split(',')

            rule_set = []
            for rule in rule_split:
                key = operation = value = destination = None
                if ':' in rule:
                    destination_split = rule.split(':')
                    destination = destination_split[1]
                    rule = destination_split[0]
                if '<' in rule or '>' in rule:
                    key = rule[0:1]
                    operation = rule[1:2]
                    value = int(rule[2:])
                if destination is None:
                    destination = rule
                rule_set.append({
                    'key': key,
                    'operation': operation,
                    'value': value,
                    'destination': destination,
                })
            rules[rule_label] = rule_set

    if not test:
        file.close()

    ranges = {
        "x": range(1, 4001),
        "m": range(1, 4001),
        "a": range(1, 4001),
        "s": range(1, 4001)
    }
    return find_ranges(ranges, "in")


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
