"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

import sys

"""
seeds:
    Map                         index
seed-to-soil map:               0
soil-to-fertilizer map:         1
fertilizer-to-water map:        2
water-to-light map:             3
light-to-temperature map:       4
temperature-to-humidity map:    5
humidity-to-location map:       6

"""
def convert_to_dicts(data):
    result = []
    for sublist in data:
        inner_result = []
        for item in sublist:
            dest, source, length = map(int, item.split())
            inner_result.append({'dest': dest, 'source': source, 'length': length})
        result.append(inner_result)
    return result

def parseFile(file):
    f = open(file, "r")
    fileStr = f.read()
    fileList = fileStr.split('\n\n')
    seeds = [int(seed) for seed in fileList[0].split(':')[1].lstrip().split(' ')]
    #print(seeds)
    mapList = fileList[1:]
    mapList = [item.split(':\n') for item in mapList]
    mapList = [line.split('\n') for line in [mapL[1] for mapL in mapList]]
    mapList = convert_to_dicts(mapList)
    return seeds, mapList

def convert_number(number, conversion_map):
    for mapping in conversion_map:
        dest_start, source_start, length = mapping['dest'], mapping['source'], mapping['length']
        if number in range(source_start, source_start + length):
            return dest_start + (number - source_start)
    return number

def find_lowest_location(seed_numbers, maps):
    for conversion_map in maps:
        # Apply the conversion for each seed number
        seed_numbers = [convert_number(seed, conversion_map) for seed in seed_numbers]
    
    # Return the lowest location number
    return min(seed_numbers)

def part1(file):
    seeds, map = parseFile(file)
    return find_lowest_location(seeds, map)
    

def create_tuples_from_list(numbers):
    # Check if the list has an odd number of elements
    if len(numbers) % 2 != 0:
        raise ValueError("Input list must have an even number of elements")

    # Create tuples of every two items in the list
    result = [(numbers[i], numbers[i + 1]) for i in range(0, len(numbers), 2)]

    return result

def convert_number2(seed, conversion_maps):
    for conversion_map in conversion_maps:
        for mapping in conversion_map:
            dest_start, source_start, length = mapping['dest'], mapping['source'], mapping['length']
            if source_start <= seed < source_start + length:
                return dest_start + (seed - source_start)
    return seed

def find_lowest_location_for_ranges(seed_ranges, conversion_maps):
    converted_numbers = []
    for seed_range in seed_ranges:
        print('checking seed', seed_range)
        current_seed_range = range(seed_range[0], seed_range[0] + seed_range[1])
        converted_numbers.extend([convert_number2(seed, conversion_maps) for seed in current_seed_range])
    return min(converted_numbers)



def build_mapping_dict2(conversion_map):
    mapping_dict = {}
    if isinstance(conversion_map[0], dict):
        # Handle the old format (list of dictionaries)
        for mapping in conversion_map:
            print('old', mapping)
            dest_start, source_start, length = mapping['dest'], mapping['source'], mapping['length']
            mapping_dict.update({i: dest_start + (i - source_start) for i in range(source_start, source_start + length)})
    else:
        # Handle the new format (list of list of dictionaries)
        for sub_map in conversion_map:
            for mapping in sub_map:
                print('new', mapping)
                dest_start, source_start, length = mapping['dest'], mapping['source'], mapping['length']
                mapping_dict.update({i: dest_start + (i - source_start) for i in range(source_start, source_start + length)})
    return mapping_dict

def build_mapping_dict(conversion_map):
    mapping_dict = {}
    for mapping in conversion_map:
        dest, source, length = mapping['dest'], mapping['source'], mapping['length']
        mapping_dict[source] = dest
    return mapping_dict


def merge_mapping_dicts(mapping_dicts):
    merged_dict = {}
    for mapping_dict in mapping_dicts:
        merged_dict.update(mapping_dict)
    return merged_dict

def fastfind(seed_ranges, conversion_maps):
    mapping_dicts = [build_mapping_dict(conversion_map) for conversion_map in conversion_maps]
    merged_mapping_dict = merge_mapping_dicts(mapping_dicts)
    
    converted_numbers = [merged_mapping_dict.get(seed, seed) for seed_range in seed_ranges for seed in range(seed_range[0], seed_range[0] + seed_range[1])]
    
    return min(converted_numbers)



class SegmentTree:
    def __init__(self, start, end, value):
        self.start = start
        self.end = end
        self.value = value
        self.left = None
        self.right = None

def build_segment_tree(mapping_dict, start, end):
    if start == end:
        return SegmentTree(start, end, mapping_dict[start])

    mid = (start + end) // 2
    left = build_segment_tree(mapping_dict, start, mid)
    right = build_segment_tree(mapping_dict, mid + 1, end)

    node = SegmentTree(start, end, min(left.value, right.value))
    node.left = left
    node.right = right

    return node

def query_segment_tree(node, start, end):
    if node.start == start and node.end == end:
        return node.value

    mid = (node.start + node.end) // 2
    if end <= mid:
        return query_segment_tree(node.left, start, end)
    elif start > mid:
        return query_segment_tree(node.right, start, end)
    else:
        return min(query_segment_tree(node.left, start, mid), query_segment_tree(node.right, mid + 1, end))

def fasterfind(seed_ranges, conversion_maps):
    mapping_dicts = [build_mapping_dict(conversion_map) for conversion_map in conversion_maps]

    for mapping_dict in mapping_dicts:
        sorted_keys = sorted(mapping_dict.keys())
        segment_tree = build_segment_tree(mapping_dict, sorted_keys[0], sorted_keys[-1])

        converted_numbers = set()
        for seed_range in seed_ranges:
            start, length = seed_range
            dest_start = query_segment_tree(segment_tree, start, start + length - 1)
            converted_numbers.update(range(dest_start, dest_start + length))

        return min(converted_numbers)



def part2(file):
    seeds, map = parseFile(file)
    seeds = create_tuples_from_list(seeds)
    #print(seeds)
    #print(map)
    return fastfind(seeds, map)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Please provide only the input file")
        sys.exit(1)
    file = sys.argv[1]
    output = part1(file)
    print("Part 1 lowest:", output)
    output2 = part2(file)
    print("Part 2 sum:", output2)