from itertools import takewhile
from common import CharacterGrid

class GroupedCharacterGrid(CharacterGrid):
    def __init__(self, lines):
        super().__init__(lines, wrapping = False, default_value = '.')

        id = 1
        self.groups = {}
        self.coord_group_map = {}
        for y in range(self.row_count):
            # Ugly, ugly. I want a C-style for loop here (to easily skip multiple iterations with x += ...)
            x = -1
            while (x := x + 1) < self.col_count:
                if not self.cell_at((x, y)).isdigit(): # type: ignore
                    continue

                # This is the first digit of a number; let's fetch the rest
                digits = list(takewhile(lambda c: c.isdigit(), self.row(y)[x:]))

                # Store the group ID for each digit
                for i in range(x, x+len(digits)):
                    self.coord_group_map[(i, y)] = id

                # Store them as a group
                value = int("".join(digits))
                self.groups[id] = value
                x += len(digits)
                id += 1

    def all_groups(self):
        """ Returns a dictionary of all groups, with the id as the key """
        return self.groups

    def group_at_coordinate(self, coordinate):
        return self.coord_group_map[coordinate]

def cell_contains_symbol(cell):
    return cell and cell != '.' and not cell.isdigit()

if __name__=='__main__':
    lines = open('data/day3.txt').read().splitlines()
    grid = GroupedCharacterGrid(lines)

    # Calculate which groups/numbers have an adjacent symbol
    groups_with_adjacent_symbol = set()
    for y in range(grid.row_count):
        for x in range(grid.col_count):
            if (c := grid.cell_at((x, y))) and c.isdigit():
                if any(cell_contains_symbol(cell) for cell in grid.neighbors((x, y))):
                    # Digit has an adjacent symbol
                    groups_with_adjacent_symbol.add(grid.group_at_coordinate((x,y)))

    # Add up all groups/numbers with an adjacent symbol
    sum = 0
    for group_id, group_value in grid.all_groups().items():
        if group_id in groups_with_adjacent_symbol:
            sum += group_value

    print(f"Part 1: {sum}")

    # Part 2: locate all *, skip if there aren't exactly two groups adjacent, multiply the two values
    sum = 0
    all_groups = grid.all_groups()
    for y in range(grid.row_count):
        for x in range(grid.col_count):
            if grid.cell_at((x, y)) == '*':
                digit_coordinates = [pair for pair in grid.neighbor_coordinates((x, y)) if (c := grid.cell_at(pair)) and c.isdigit()]
                group_ids = {grid.group_at_coordinate(coordinate) for coordinate in digit_coordinates}

                # Skip if there aren't exactly two groups adjacent
                if len(group_ids) != 2:
                    continue

                # Extract the two groups/numbers and multiply them
                a, b = group_ids
                ratio = all_groups[a] * all_groups[b]
                sum += ratio

    print(f"Part 2: {sum}")