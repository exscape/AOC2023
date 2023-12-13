import itertools
from common import CharacterGrid

def find_reflection(line_func, line_count, smudge = False):
    def differences(line_a, line_b):
        """ How many characters differ in these strings? """
        return len(line_a) - sum(1 for i in range(len(line_a)) if line_a[i] == line_b[i])

    for reflection_line in range(1, line_count):
        misses = 0
        for offset in range(0, line_count // 2):
            a = reflection_line - offset - 1
            b = reflection_line + offset
            if a >= 0 and b < line_count:
                line_a = line_func(a)
                line_b = line_func(b)
                if smudge and differences(line_a, line_b) == 1:
                    # This didn't match, but there was exactly one single mismatch so far, so keep going
                    misses += 1
                elif line_a != line_b:
                    break
        else:
            # The loop finished without breaking, so this could be a match
            if not smudge or misses == 1:
                return reflection_line

    return 0

def solve(grids, smudge):
    sum = 0
    for grid in grids:
        sum += 100 * (reflection_line := find_reflection(grid.row, grid.row_count, smudge))
        if reflection_line == 0:
            sum += find_reflection(grid.col, grid.col_count, smudge)

    return sum

if __name__=='__main__':
    lines = open('data/day13.txt').read().splitlines()
    grids = [CharacterGrid(list(g), default_value=None) for k, g in itertools.groupby(lines, bool) if k]

    print(f"Part 1: {solve(grids, smudge=False)}")
    print(f"Part 2: {solve(grids, smudge=True)}")