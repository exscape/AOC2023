import itertools
from common import CharacterGrid, taxicab_distance

class GalaxyGrid(CharacterGrid):
    def find_empty_rows(self):
        return [i for i, row in enumerate(self.rows())
                if all(cell == '.' for cell in row)]

    def find_empty_cols(self):
        return [i for i, col in enumerate(self.cols())
                if all(cell == '.' for cell in col)]

    def expand(self):
        """ Duplicate empty rows and column to simulate dark energy expansion """
        empty_rows = self.find_empty_rows()
        empty_cols = self.find_empty_cols()

        for r in reversed(empty_rows):
            self.insert_row(r, ['.'] * self.col_count)

        for c in reversed(empty_cols):
            self.insert_col(c, ['.'] * self.row_count)

def solve_part1(lines):
    """ Actually expand the grid. I could of course use the part 2 solution here, too. """
    grid = GalaxyGrid(lines, wrapping=False, default_value='.')
    grid.expand()
    galaxy_positions = [position for position in grid.coordinate_pairs() if grid.cell_at(position) == '#']
    galaxy_pairs = list(itertools.combinations(galaxy_positions, 2))

    return sum(taxicab_distance(a, b) for a, b in galaxy_pairs)

def solve_part2(lines):
    """ Simulate expansion by modifying the galaxy coordinates accordingly """
    grid = GalaxyGrid(lines, wrapping=False, default_value='.')
    galaxy_positions = [position for position in grid.coordinate_pairs() if grid.cell_at(position) == '#']

    for r in reversed(grid.find_empty_rows()):
        for i in range(len(galaxy_positions)):
            if (pos := galaxy_positions[i])[1] > r:
                galaxy_positions[i] = (pos[0], pos[1] + 999999)

    for c in reversed(grid.find_empty_cols()):
        for i in range(len(galaxy_positions)):
            if (pos := galaxy_positions[i])[0] > c:
                galaxy_positions[i] = (pos[0] + 999999, pos[1])

    galaxy_pairs = list(itertools.combinations(galaxy_positions, 2))

    return sum(taxicab_distance(a, b) for a, b in galaxy_pairs)

if __name__=='__main__':
    lines = open('data/day11.txt').read().splitlines()
    print(f"Part 1: {solve_part1(lines)}")
    print(f"Part 2: {solve_part2(lines)}")