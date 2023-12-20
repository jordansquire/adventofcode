from util.util import timeit

test_data1 = [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a',
]
test_data2 = [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output',
]
flip = {}
conjunction = {}
broadcast = []
pulse_queue = []
count = {'high_count': 0, 'low_count': 0}


def push_button():
    count['low_count'] += 1
    for out in broadcast:
        enqueue('broadcaster', out, False)


def enqueue(source, dest, pulse):
    pulse_queue.append({'source': source, 'dest': dest, 'pulse': pulse})
    if pulse:
        count['high_count'] += 1
    else:
        count['low_count'] += 1
    # print(f'{source} -{pulse}-> {dest}')


def do_flip(flip_name, pulse):
    if pulse:  # Do nothing for high pulse
        return

    flip[flip_name]['on'] = not flip[flip_name]['on']
    for out in flip[flip_name]['output']:
        enqueue(flip_name, out, flip[flip_name]['on'])


def do_conjunction(conj_name, input_name, pulse):
    conjunction[conj_name]['input'][input_name] = pulse
    output_pulse = False
    for input in conjunction[conj_name]['input']:
        if not conjunction[conj_name]['input'][input]:
            output_pulse = True
            break

    for out in conjunction[conj_name]['output']:
        enqueue(conj_name, out, output_pulse)


def find_inputs():
    for conj in conjunction:
        for broad in broadcast:
            if broad == conj:
                conjunction[conj]['input']['broadcaster'] = False
        for f in flip:
            for out in flip[f]['output']:
                if out == conj:
                    conjunction[conj]['input'][f] = False
        for c in conjunction:
            for out in conjunction[c]['output']:
                if out == conj:
                    conjunction[conj]['input'][c] = False


@timeit
def calculate_score(test: bool, iterations) -> int:
    if test:
        file = test_data2
    else:
        file = open("input.txt", "r")

    for line in file:
        line_split = line.strip().split(' -> ')
        if line_split[0] == 'broadcaster':
            for dest in line_split[1].split(', '):
                broadcast.append(dest)
        if '%' in line_split[0]:
            flip[line_split[0][1:]] = {'output': line_split[1].split(', '), 'on': False}
        if '&' in line_split[0]:
            conjunction[line_split[0][1:]] = {'input': {}, 'output': line_split[1].split(', ')}

    if not test:
        file.close()

    find_inputs()
    for _ in range(iterations):
        push_button()
        while pulse_queue:
            operation = pulse_queue.pop(0)
            if operation['dest'] in flip:
                do_flip(operation['dest'], operation['pulse'])
            if operation['dest'] in conjunction:
                do_conjunction(operation['dest'], operation['source'], operation['pulse'])

    print(f"low_count: {count['low_count']} high_count: {count['high_count']}")
    return count['high_count'] * count['low_count']


if __name__ == '__main__':
    score = calculate_score(test=False, iterations=1000)
    print(f'Score: {score}')
