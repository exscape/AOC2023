import re
import operator
import itertools
from dataclasses import dataclass

@dataclass
class Mapping:
    """ A single map range, e.g. map values from [40,50] to [65,75] """
    src: int
    offset: int
    length: int

    def __init__(self, s):
        (dest, self.src, self.length) = [int(n) for n in s.split(" ")]
        self.offset = dest - self.src

@dataclass
class Map:
    """ A map from one value type to another, e.g. seed-to-soil or soil-to-fertilizer. Contains many mappings (ranges). """
    mappings: list[Mapping]

    def __init__(self, mappings):
        self.mappings = sorted(mappings, key=operator.attrgetter("src"))

    def lookup(self, value):
        """ Convert a value by looking it up in the appropriate mapping. """
        for m in self.mappings:
            if value >= m.src and value < m.src + m.length:
                return value + m.offset
        return value
    
    def overhead(self, value):
        """ How much higher could value be, and still fit within the same mapping? """

        if value < self.mappings[0].src:
            # Value is lower than all existing mappings. Return the distance up to the first mapping.
            return self.mappings[0].src - value - 1
        elif value >= self.mappings[-1].src + self.mappings[-1].length:
            # Value is higher than all existing mappings. Overhead is infinite here.
            return float('inf')

        # Handle the case where value falls into one of the mappings
        for m in self.mappings:
            if value >= m.src and value < m.src + m.length:
                return m.src + m.length - value - 1

        # Value must be in between two existing mappings.
        # Find the first mapping that has src > value and return the distance to that.
        for m in self.mappings:
            if m.src > value:
                return m.src - value

        # Should never be reached!
        assert(False)

@dataclass
class SeedRange:
    start: int
    length: int

def parse_input(filename):
    NUMBER_REGEX = re.compile(r'\d+')
    lines = open(filename).read().splitlines()

    # For part 1
    seeds = [int(n) for n in NUMBER_REGEX.findall(lines[0])]
    # For part 2
    seed_ranges = [SeedRange(*x) for x in itertools.batched(seeds, 2)]

    # Group the lines into the different maps (like splitting a string on whitespace)
    def starts_with_digit(line):
        return len(line) > 0 and line[0].isdigit()
    grouped_lines = [list(group) for is_data_line, group in itertools.groupby(lines[2:], key=starts_with_digit) if is_data_line]

    maps: list[Map] = []
    for group in grouped_lines:
        # group now looks something like: ['50 98 2', '52 50 48']
        # Each entry in such a list becomes a Mapping, and all of them together become a Map (e.g. a seed-to-soil map).
        # This loop *could* be replaced with a one-liner, but I think that would be pushing it too far.
        maps.append(Map([Mapping(g) for g in group]))
    
    return (seeds, seed_ranges, maps)

def location_from_seed(seed, maps):
    """ Perform a lookup using each map in turn. """
    value = seed
    for m in maps:
        value = m.lookup(value)
    return value

if __name__=='__main__':
    (seeds, seed_ranges, maps) = parse_input('data/day5.txt')

    # Part 1
    # Simply run location_from_seed on each seed, and pick the lowest value.
    print(f"Part 1: {min([location_from_seed(seed, maps) for seed in seeds])}")

    # Part 2
    # Calculate a set of seed ranges that all use the same "mapping path", so to speak.
    # Only the lowest value in such a range could possibly yield the lowest possible
    # location number, so after calculating the ranges, we only test the lowest/first value
    # in each range.
    seeds = []
    for sr in seed_ranges:
        max_overhead = 0
        mapped_start = sr.start
        for m in maps:
            overhead = m.overhead(mapped_start)
            max_overhead = min(overhead, max_overhead) if max_overhead > 0 else overhead

            # Apply the offset from the map
            mapped_start = m.lookup(mapped_start)

        seeds.append(sr.start)

        # If we didn't process the entire SeedRange, add the rest for later processing
        if max_overhead < sr.length:
            seed_ranges.append(SeedRange(sr.start + int(max_overhead) + 1, sr.length - int(max_overhead) - 1))

    # We finally have the seed values. Map each of them to a location and extract the lowest value.
    print(f"Part 2: {min([location_from_seed(seed, maps) for seed in seeds])}")