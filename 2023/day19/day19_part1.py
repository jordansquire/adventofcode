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
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}',
]
rules = {}
parts = []


def do_operation(value, operation, rule_value) -> bool:
    if operation == '<':
        return value < rule_value
    if operation == '>':
        return value > rule_value
    return False


def check_rules(part) -> int:
    rule_set = rules['in']
    while True:
        for rule in rule_set:
            if rule['key'] is not None:
                if not do_operation(part[rule['key']], rule['operation'], rule['value']):
                    continue

            if rule['destination'] == 'A':
                return part['x'] + part['m'] + part['a'] + part['s']

            if rule['destination'] == 'R':
                return 0

            rule_set = rules[rule['destination']]
            break


def process_parts_and_rules() -> int:
    part_total = 0
    for part in parts:
        part_total += check_rules(part)
    return part_total



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

        else:
            part = {}
            line = line.replace('{', '').replace('}', '')
            line_split = line.split(',')
            for category in line_split:
                category_split = category.split('=')
                part[category_split[0]] = int(category_split[1])
            parts.append(part)

    if not test:
        file.close()

    return process_parts_and_rules()


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
