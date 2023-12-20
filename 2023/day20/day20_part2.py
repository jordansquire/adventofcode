from math import lcm
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
def calculate_score(test: bool) -> int:
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
    watch_nodes = {
        'pl': -1,
        'mz': -1,
        'lz': -1,
        'zm': -1,
    }

    button_count = 0
    while True:
        button_count += 1
        push_button()
        while pulse_queue:
            operation = pulse_queue.pop(0)

            # Generate cadences and find the LCM
            if operation['source'] in watch_nodes and operation['dest'] == 'bn' and operation['pulse']:
                if watch_nodes[operation['source']] == -1:
                    watch_nodes[operation['source']] = button_count
                cadence_set = []
                for node in watch_nodes:
                    if watch_nodes[node] != -1:
                        cadence_set.append(watch_nodes[node])
                if len(cadence_set) == len(watch_nodes):
                    print(cadence_set)
                    return lcm(*cadence_set)

            if operation['dest'] in flip:
                do_flip(operation['dest'], operation['pulse'])
            if operation['dest'] in conjunction:
                do_conjunction(operation['dest'], operation['source'], operation['pulse'])


if __name__ == '__main__':
    score = calculate_score(test=False)
    print(f'Score: {score}')
