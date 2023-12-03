############ BRYT UT TILL EGEN FIL ##############

from typing import Any, Sequence, Generic, TypeVar

class Cell:
    def __init__(self, contents: Any):
        self.contents = contents

    def __repr__(self):
        return f"{self.contents}"

T = TypeVar('T', bound=Cell)

class GenericGrid(Generic[T]):
    def __init__(self, data: Sequence[Sequence[T]], wrapping = False, default_value = None):
        self.data = data
        self.row_count = len(self.data)
        self.col_count = len(self.data[0]) if len(self.data) > 0 else 0

        # If wrapping = True, accessing one to the right of the rightmost column will wrap to the leftmost column, and so on
        # If wrapping = False, the grid is padded in all directions by infinitely many default_value cells
        self.wrapping = wrapping
        self.default_value = default_value

    def row(self, y) -> Sequence[T]:
        return self.data[y]

    def rows(self) -> Sequence[Sequence[T]]:
        return self.data

    def cols(self) -> Sequence[Sequence[T]]:
        # TODO: implement
        assert(False)

    def cell_at(self, x, y) -> T | None:
        if x >= 0 and y >= 0 and x < self.col_count and y < self.row_count:
            return self.data[y][x]
        elif self.wrapping:
            # TODO: implement -- using Python's default indexing behavior where possible
            assert(False)
        elif x < 0 or y < 0:
            return None
        else:
            # Not wrapping and x >= self.col_count or y >= self.row_count
            return None
    
    def contents_at(self, x, y) -> Any:
        cell = self.cell_at(x, y)
        return cell.contents if cell else self.default_value

    def neighbors(self, x, y) -> list[T | None]:
        """ Return a list of all neighboring cells, wrapping or inserting default valued cells if needed. """
        cells = []
        for offset_x in (-1, 0, 1):
            for offset_y in (-1, 0, 1):
                if not (offset_x == 0 and offset_y == 0):
                    cells.append(self.cell_at(x + offset_x, y + offset_y))

        assert(len(cells) == 8)
        return cells

class CharacterGrid(GenericGrid):
    """ Each cell is one character, usually ASCII, created from a list of strings """
    def __init__(self, lines: Sequence[str], wrapping = False, default_value = None):
        data: list[list[Cell]] = []
        for line in lines:
            row = list(map(Cell, list(line)))
            data.append(row)

        super().__init__(data, wrapping, default_value)

    def print(self):
        for row in self.data:
            print(''.join(map(lambda c: c.contents, row)))

############ SLUT BRYT UT TILL EGEN FIL ##############

from itertools import takewhile

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
                digits = list(map(lambda c: c.contents, digit_cells))
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
                digits = filter(lambda c: c and c.contents.isdigit(), grid.neighbors(x, y))
                group_ids = set(map(lambda c: c.group_id, digits))

                # Skip if there aren't exactly two groups adjacent
                if len(group_ids) != 2:
                    continue

                # Extract the two groups/numbers and multiply them
                a, b = group_ids
                ratio = all_groups[a] * all_groups[b]
                sum += ratio

    print(f"Part 2: {sum}")