############ BRYT UT TILL EGEN FIL ##############

from typing import Any, Sequence

class Cell:
    def __init__(self, contents: Any):
        self.contents = contents

    def __repr__(self):
        return f"{self.contents}"

class GenericGrid:
    def __init__(self, data: Sequence[Sequence[Cell]], wrapping = False, default_value = None):
        self.data = data
        self.row_count = len(self.data)
        self.col_count = len(self.data[0]) if len(self.data) > 0 else 0

        # If wrapping = True, accessing one to the right of the rightmost column will wrap to the leftmost column, and so on
        # If wrapping = False, the grid is padded in all directions by infinitely many default_value cells
        self.wrapping = wrapping
        self.default_value = default_value

    def row(self, y) -> Sequence[Cell]:
        return self.data[y]

    def rows(self) -> Sequence[Sequence[Cell]]:
        return self.data

    def cols(self) -> Sequence[Sequence[Cell]]:
        # TODO: implement
        assert(False)

    def cell_at(self, x, y) -> Cell | None:
        if x >= 0 and y >= 0 and x < self.col_count and y < self.row_count:
            return self.data[y][x]
        elif self.wrapping:
            # TODO: implement -- using Python's default indexing behavior where possible
            assert(False)
        elif x < 0 or y < 0:
            # TODO: should this return None or an empty Cell (e.g. Cell.empty == True)?
            return None
        else:
            # Not wrapping and x >= self.col_count or y >= self.row_count
            # TODO: should this return None or an empty Cell (e.g. Cell.empty == True)?
            return None
    
    def contents_at(self, x, y) -> Any:
        cell = self.cell_at(x, y)
        return cell.contents if cell else self.default_value

    def neighbors(self, x, y) -> list[Cell | None]:
        """ Return a list of all neighboring cells, wrapping or inserting default valued cells if needed. """
        cells = []
        for offset_x in (-1, 0, 1):
            for offset_y in (-1, 0, 1):
                if not (offset_x == 0 and offset_y == 0):
                    cells.append(self.cell_at(x + offset_x, y + offset_y))

        assert(len(cells) == 8)
        return cells

# Each cell is one byte, usually ASCII, read from text
class ByteGrid(GenericGrid):
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

class GroupedByteGrid(ByteGrid):
    def __init__(self, lines):
        super().__init__(lines, wrapping = False, default_value = '.')

        # Add a group ID to each digit (all consecutive digits belong to the same group)
        group_id = 0
        for row in self.data:
            newGroup = True
            for cell in row:
                if cell.contents.isdigit():
                    if newGroup:
                        group_id += 1
                        newGroup = False
                    cell.group_id = group_id
                else:
                    cell.group_id = None
                    newGroup = True

    def all_groups(self):
        """ Returns a list of all groups in the form [(id, value), ...]"""
        groups = []
        id = 1
        for y in range(grid.row_count):
            # Ugly, ugly. I want a C-style for loop here (to easily skip multiple iterations with x += ...)
            x = -1
            while (x := x + 1) < grid.col_count:
                if not grid.contents_at(x, y).isdigit():
                    continue

                # This is the first digit of a number; let's fetch the rest
                digits = list(map(lambda c: c.contents, takewhile(lambda c: c.contents.isdigit(), grid.row(y)[x:])))
                value = int("".join(digits))
                groups.append( (id, value) )
                x += len(digits)
                id += 1

        return groups

lines = open('data/day3.txt').read().splitlines()

grid = GroupedByteGrid(lines)

def cell_contains_symbol(cell):
    return cell and cell.contents != '.' and not cell.contents.isdigit() 

count = 0
groups_with_adjacent = set()
for y in range(grid.row_count):
    for x in range(grid.col_count):
        if (c := grid.cell_at(x, y)) and c.contents.isdigit():
            if any([cell_contains_symbol(cell) for cell in grid.neighbors(x, y)]):
                # Digit has an adjacent symbol
                groups_with_adjacent.add(c.group_id)

sum = 0
for group_id, group_value in grid.all_groups():
    if group_id in groups_with_adjacent:
        sum += group_value

print(f"Part 1: {sum}")