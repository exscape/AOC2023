import re
from dataclasses import dataclass
import itertools

# The problem description, example data and actual problem data all have the same maps
# in the same order. Therefore, this is coded to apply each map in order,
# rather than doing some ugly nested lookup with proper names, like
# humidity_to_location[temperature_to_humidity[light_to_temperature[...]]]

@dataclass
class Mapping:
    dest: int
    src: int
    length: int

    def __init__(self, s):
        (self.dest, self.src, self.length) = map(int, s.split(" "))

@dataclass
class Map:
    mappings: list[Mapping]

    def lookup(self, value):
        for m in self.mappings:
            if value >= m.src and value < m.src + m.length:
                return m.dest + (value - m.src)
        return value

def starts_with_digit(line):
    return len(line) > 0 and line[0].isdigit()

NUMBER_REGEX = re.compile(r'\d+')

lines = open('data/day5.txt').read().splitlines()
seeds = map(int, NUMBER_REGEX.findall(lines[0]))
lines = lines[2:]

# "Split" the lines into the different maps
grouped_lines = [list(group) for is_data_line, group in itertools.groupby(lines, key=starts_with_digit) if is_data_line]

maps = []
for group in grouped_lines:
    # group now looks something like: ['50 98 2', '52 50 48']
    # Each list entry becomes a Mapping, and all of them together become a Map
    # So, somewhat confusingly, we use Python's map() to to create a list of Mapping instances, stored in a Map.
    # This loop *could* be replaced with a one-liner, but I think that would be pushing it too far.
    maps.append(Map(list(map(Mapping, group))))

locations = []
for seed in seeds:
    # Apply each map in turn to the seed number
    location = seed
    for m in maps:
        location = m.lookup(location)
    locations.append(location)
    
print(f"Part 1: {min(locations)}")