from itertools import takewhile

from common import CharacterGrid

class GroupedCharacterGrid(CharacterGrid):
    def __init__(self, lines):
        super().__init__(lines, wrapping = False, default_value = '.')

        id = 1
        self.groups = {}
        for y in range(self.row_count):
            # Ugly, ugly. I want a C-style for loop here (to easily skip multiple iterations with x += ...)
            x = -1
            while (x := x + 1) < self.col_count:
                if not self.contents_at(x, y).isdigit():
                    continue

                # This is the first digit of a number; let's fetch the rest
                digit_cells = list(takewhile(lambda c: c.contents.isdigit(), self.row(y)[x:]))

                # Set the group ID for each digit
                for digit_cell in digit_cells:
                    digit_cell.group_id = id

                # Store them as a group
                digits = [c.contents for c in digit_cells]
                value = int("".join(digits))
                self.groups[id] = value
                x += len(digits)
                id += 1

    def all_groups(self):
        """ Returns a dictionary of all groups, with the id as the key """
        return self.groups

def cell_contains_symbol(cell):
    return cell and cell.contents != '.' and not cell.contents.isdigit() 

if __name__=='__main__':
    lines = open('data/day3.txt').read().splitlines()
    grid = GroupedCharacterGrid(lines)

    # Calculate which groups/numbers have an adjacent symbol
    groups_with_adjacent_symbol = set()
    for y in range(grid.row_count):
        for x in range(grid.col_count):
            if (c := grid.cell_at(x, y)) and c.contents.isdigit():
                if any([cell_contains_symbol(cell) for cell in grid.neighbors(x, y)]):
                    # Digit has an adjacent symbol
                    groups_with_adjacent_symbol.add(c.group_id)

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
            if (c := grid.cell_at(x, y)) and c.contents == '*':
                digits = [cell for cell in grid.neighbors(x, y) if cell and cell.contents.isdigit()]
                group_ids = {c.group_id for c in digits}

                # Skip if there aren't exactly two groups adjacent
                if len(group_ids) != 2:
                    continue

                # Extract the two groups/numbers and multiply them
                a, b = group_ids
                ratio = all_groups[a] * all_groups[b]
                sum += ratio

    print(f"Part 2: {sum}")