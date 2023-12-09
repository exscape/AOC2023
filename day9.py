import itertools
from collections import deque

def extrapolate_history(history):
    # Generate a list of differences: [[1, 3, 6, 10, 15, 21], [2, 3, 4, 5, 6], [1, 1, 1, 1], [0, 0, 0]]
    # diffs[0] contains the original values, followed by each set of differences in turn
    diffs = [deque(history)]
    while not all([x == 0 for x in diffs[-1]]):
        diffs.append(deque([b-a for (a, b) in itertools.pairwise(diffs[-1])]))

    # Work backwards through the lists adding up values
    for current, previous in itertools.pairwise(reversed(diffs)):
        previous.append(current[-1] + previous[-1])
        previous.appendleft(previous[0] - current[0])

    return diffs[0]

def solve(histories):
    histories = [extrapolate_history(history) for history in histories]
    return [sum([h[-1] for h in histories]), sum([h[0] for h in histories])]

if __name__=='__main__':
    lines = open('data/day9.txt').read().splitlines()
    histories = [[int(n) for n in history] for history in [line.split(" ") for line in lines]]

    (part1, part2) = solve(histories)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
