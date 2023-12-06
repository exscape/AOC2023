import re
from dataclasses import dataclass

@dataclass
class Race:
    length: int
    record: int

def ways_to_win_race(race):
    ways_to_win = 0
    for hold_time in range(1, race.length):
        speed = hold_time # mm/s
        length = speed * (race.length - hold_time)
        if length > race.record:
            ways_to_win += 1
    return ways_to_win

if __name__=='__main__':
    lines = open('data/day6.txt').read().splitlines()
    NUMBER_REGEX = re.compile(r'\d+')
    times = NUMBER_REGEX.findall(lines[0])
    records = NUMBER_REGEX.findall(lines[1])
    races = list(map(lambda x: Race(*map(int, x)), zip(times, records)))

    part_2_race = Race(int("".join(times)), int("".join(records)))

    prod = 1
    for race in races:
        prod *= ways_to_win_race(race)

    print(f"Part 1: {prod}")
    print(f"Part 2: {ways_to_win_race(part_2_race)}")
