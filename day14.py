# pyright: reportOptionalMemberAccess=false
import itertools
from copy import deepcopy
from common import CharacterGrid

class StoneGrid(CharacterGrid):
    def tilt(self):
        for x in range(self.col_count):
            groups = [list(g) for _, g in itertools.groupby(self.col(x), lambda cell: cell.contents != '#')]
            groups = [sorted(group, key=lambda x: x.contents, reverse=True) for group in groups]
            new_col = itertools.chain.from_iterable(groups) # flatten

            for y, cell in enumerate(new_col):
                self.data[y][x] = cell

    def perform_cycle(self):
        for _ in range(4):
            self.tilt()
            self.rotate()

    def north_beam_load(self):
        return sum((self.row_count - y) * [c.contents for c in self.row(y)].count('O') for y in range(self.row_count))

def solve(lines):
    # Part 1
    grid = StoneGrid(lines)
    grid.tilt()
    part1 = grid.north_beam_load()

    # Part 2
    grid = StoneGrid(lines)
    seen_grids = []

    for i in range(1_000_000_000):
        seen_grids.append(deepcopy(grid))
        grid.perform_cycle()

        if grid in seen_grids:
            prev_index = seen_grids.index(grid) - 1
            cycle_length = i - prev_index
            answer_index = prev_index + ((1_000_000_000_000) - prev_index) % cycle_length
            part2 = seen_grids[answer_index].north_beam_load()

            return (part1, part2)

if __name__=='__main__':
    lines = open('data/day14.txt').read().splitlines()
    print("This will take a while...")
    part1, part2 = solve(lines)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")