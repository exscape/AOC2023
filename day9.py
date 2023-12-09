import itertools

def solve(histories):
    last_values = []
    for history in histories:
        # Generate a list of differences: [[1, 3, 6, 10, 15, 21], [2, 3, 4, 5, 6], [1, 1, 1, 1], [0, 0, 0]]
        diffs = [history]
        while not all([x == 0 for x in diffs[-1]]):
            diffs.append([b-a for (a, b) in itertools.pairwise(diffs[-1])])

        diffs[-1].append(0) # TODO: is this really necessary? I can't see how

        # Start working backwards through the lists
        for i in range(-1, -len(diffs), -1):
            # Append to the previous list: last value of this list + last value of the previous list
            diffs[i-1].append(diffs[i][-1] + diffs[i-1][-1])

        last_values.append(diffs[0][-1])
    return sum(last_values)

if __name__=='__main__':
    lines = open('data/day9.txt').read().splitlines()
    histories = [[int(n) for n in history] for history in [line.split(" ") for line in lines]]

    answer = solve(histories)
    print(f"Part 1: {answer}")
