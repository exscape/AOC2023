import re
import math
from collections import defaultdict

lines = open('data/day2.txt', 'r').read().splitlines()

GAME_REGEX = re.compile('[:;] ')
COLOR_REGEX = re.compile('(\d+) (red|green|blue)')

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14

game_id_sum = 0
power_sum = 0

for game in lines:
    id, *picks = GAME_REGEX.split(game)
    id = int(id[5:])
    game_possible = True
    min_required = defaultdict(int)

    for pick in picks:
        color_map = defaultdict(int)

        # Split picks into a list e.g. [(3, 'red'), (2, 'green')],
        # and transform into a dict e.g. {'red': 3, 'green': 2}
        for color_matches in COLOR_REGEX.findall(pick):
            v, k = color_matches
            color_map[k] = int(v)

        # Part 1
        if color_map['red'] > RED_MAX or color_map['green'] > GREEN_MAX or color_map['blue'] > BLUE_MAX:
            game_possible = False

        # Part 2
        for color in ('red', 'green', 'blue'):
            min_required[color] = max(min_required[color], color_map[color])
    
    # Part 1
    if game_possible:
        game_id_sum += id

    # Part 2
    power = math.prod(min_required.values())
    power_sum += power

print(f'Part 1: {game_id_sum}')
print(f'Part 2: {power_sum}')