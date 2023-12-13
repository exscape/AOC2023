import itertools
from common import CharacterGrid

def find_reflection(line_func, line_count):
    # Check for reflected lines *above* this index, which always leaves at least one line on either side of the reflection axis
    # TODO: better limits, this goes out of bounds to figure out where to stop
    for reflection_line in range(1, line_count):
        for offset in range(0, line_count):
            if (a:=line_func(reflection_line - offset - 1)) != (b:=line_func(reflection_line + offset)) \
                and not (all(x==None for x in a) or all(x==None for x in b)):
                # These don't match, AND neither of the lines is out of bounds, so there's no reflection here, try another line
                break
            if all(x==None for x in a) and all(x==None for x in b):
                # We reached outside the bounds on both sides, without finding a difference, so we found the reflection line
                return reflection_line

    return 0

def solve(grids):
    grids = [CharacterGrid(grid_data, default_value=None) for grid_data in grids]

    sum = 0
    for grid in grids:
        sum += 100 * (reflection_line := find_reflection(grid.row, grid.row_count))
        if reflection_line == 0:
            sum += find_reflection(grid.col, grid.col_count)

    return sum

if __name__=='__main__':
    lines = open('data/day13.txt').read().splitlines()
    grids = [list(g) for k, g in itertools.groupby(lines, bool) if k]

    print(f"Part 1: {solve(grids)}")