import concurrent.futures
import queue
import threading

test_data = [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4'
]

seed_spliter = []
seeds = []
seed_to_soil = []
soil_to_fertilizer = []
fertilizer_to_water = []
water_to_light = []
light_to_temperature = []
temperature_to_humidity = []
humidity_to_location = []
min_location = None


def seed_producer(seed_queue):
    seed_split = seed_spliter[0]
    for index in range(0, int(len(seed_split) / 2)):
        seed_start = int(seed_split[index * 2])
        seed_len = int(seed_split[index * 2 + 1])
        for seed in range(seed_start, seed_start + seed_len + 1):
            seed_queue.put(seed)

    print(f'Seed production complete')
    seed_queue.put(-1)


def generate_maps(test: bool):
    if test:
        file = test_data
    else:
        file = open("input.txt", "r")

    first = True
    target_map = []
    for line in file:
        if first:
            seed_spliter.append(line.split(':')[1].split())
            first = False
            continue

        if line.strip() == "":
            continue

        if not line[0].isnumeric():
            if line[0:4] == 'seed':
                target_map = seed_to_soil
            if line[0:4] == 'soil':
                target_map = soil_to_fertilizer
            if line[0:4] == 'fert':
                target_map = fertilizer_to_water
            if line[0:4] == 'wate':
                target_map = water_to_light
            if line[0:4] == 'ligh':
                target_map = light_to_temperature
            if line[0:4] == 'temp':
                target_map = temperature_to_humidity
            if line[0:4] == 'humi':
                target_map = humidity_to_location
            continue

        line_split = line.split()
        dest_start = int(line_split[0])
        source_start = int(line_split[1])
        length = int(line_split[2])
        target_map.append(
            {
                'src_start': source_start,
                'dest_start': dest_start,
                'length': length
            }
        )

    # print(seeds)
    # print(seed_to_soil)
    # print(soil_to_fertilizer)
    # print(fertilizer_to_water)
    # print(water_to_light)
    # print(light_to_temperature)
    # print(temperature_to_humidity)
    # print(humidity_to_location)

    if not test:
        file.close()


def map_evaluate(mapping, input_val) -> int:
    for map in mapping:
        if map['src_start'] <= input_val < map['src_start'] + map['length']:
            return map['dest_start'] + input_val - map['src_start']
    return input_val


def find_closest_location(queue, event):
    global min_location
    seed_count = 0
    while not event.is_set() or not queue.empty():
        seed = queue.get()
        if seed == -1:
            event.set()
            break

        soil = map_evaluate(seed_to_soil, seed)
        fertilizer = map_evaluate(soil_to_fertilizer, soil)
        water = map_evaluate(fertilizer_to_water, fertilizer)
        light = map_evaluate(water_to_light, water)
        temperature = map_evaluate(light_to_temperature, light)
        humidity = map_evaluate(temperature_to_humidity, temperature)
        location = map_evaluate(humidity_to_location, humidity)

        # print(f'Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}.')

        if min_location is None or location < min_location:
            min_location = location

        seed_count += 1
        if seed_count % 1_000_000 == 0:
            print(f'Processed {seed_count} seeds')


if __name__ == '__main__':
    generate_maps(test=False)

    seed_queue = queue.Queue(maxsize=10_000)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.submit(seed_producer, seed_queue)
        for x in range(0, 98):
            executor.submit(find_closest_location, seed_queue, event)

    print(f'Closest Location: {min_location}')