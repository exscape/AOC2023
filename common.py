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