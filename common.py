from typing import Any, Generic, TypeVar, Tuple

class Cell:
    def __init__(self, contents: Any, position = None):
        self.contents = contents
        self.position = position

    def __repr__(self):
        return f"{self.contents}"

    def __eq__(self, other):
        if other:
            return self.contents == other.contents
        else:
            return False

T = TypeVar('T', bound=Cell)

def taxicab_distance(from_: Tuple[int, int], to: Tuple[int, int]):
    return abs(from_[0] - to[0]) + abs(from_[1] - to[1])

class GenericGrid(Generic[T]):
    def __init__(self, data: list[list[T]], wrapping = False, default_value: Any = None):
        self.data = list(data)
        self.row_count = len(self.data)
        self.col_count = len(self.data[0]) if len(self.data) > 0 else 0

        # If wrapping = True, accessing one to the right of the rightmost column will wrap to the leftmost column, and so on
        # If wrapping = False, the grid is padded in all directions by infinitely many default_value cells
        self.wrapping = wrapping
        self.default_value = default_value

    @classmethod
    def wrap_coordinate(cls, c, max_count):
        """ Transform a coordinate to allow for infinite wrapping, e.g. grid.row(-123) for a 50-row grid """
        if c >= max_count:
            c = c % max_count
        elif c <= -max_count:
            c = c % -max_count
        return c

    def row(self, y) -> list[T|None]:
        if y >= 0 and y < self.row_count:
            return self.data[y]
        elif self.wrapping:
            y = GenericGrid.wrap_coordinate(y, self.row_count)
            return self.data[y]
        else:
            return [None] * self.col_count

    def col(self, x) -> list[T|None]:
        if x >= 0 and x < self.col_count:
            return [self.data[y][x] for y in range(self.row_count)]
        elif self.wrapping:
            x = GenericGrid.wrap_coordinate(x, self.col_count)
            return [self.data[y][x] for y in range(self.row_count)]
        else:
            return [None] * self.row_count

    def rows(self) -> list[list[T]]:
        return self.data

    def cols(self) -> list[list[T]]:
        return [list(x) for x in zip(*self.data)]

    def cell_at(self, position: Tuple[int, int]) -> T | None:
        (x, y) = position
        if x >= 0 and y >= 0 and x < self.col_count and y < self.row_count:
            return self.data[y][x]
        elif self.wrapping:
            # Allow infinite wrapping in all directions
            x = GenericGrid.wrap_coordinate(x, self.col_count)
            y = GenericGrid.wrap_coordinate(y, self.row_count)
            return self.data[y][x]
        else:
            # Not wrapping and out of bounds
            return None

    def contents_at(self, position: Tuple[int, int]) -> Any:
        cell = self.cell_at(position)
        return cell.contents if cell else self.default_value

    def neighbors(self, position: Tuple[int, int], include_diagonals=True) -> list[T | None]:
        """ Return a list of all neighboring cells, wrapping or inserting default valued cells if needed. """
        cells = []
        (x, y) = position
        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                if not include_diagonals and abs(offset_x) == 1 and abs(offset_y) == 1:
                    continue
                cells.append(cell := self.cell_at((x + offset_x, y + offset_y)))
                if cell:
                    assert(cell.position == (x + offset_x, y + offset_y))

        assert(len(cells) == 8 if include_diagonals else 4)
        return cells

    def insert_row(self, before_row, new_cells):
        assert(self.row_count >= before_row)
        assert(len(new_cells) == self.col_count)
        self.data.insert(before_row, new_cells)
        self.row_count += 1
        self.recalculate_positions()

    def insert_col(self, before_col, new_cells):
        assert(self.col_count >= before_col)
        assert(len(new_cells) == self.row_count)

        for y in range(self.row_count):
            self.data[y].insert(before_col, new_cells[y])

        self.col_count += 1
        self.recalculate_positions()

    def recalculate_positions(self):
        """ Update the position value of each Cell """
        for y in range(self.row_count):
            for x in range(self.col_count):
                cell = self.cell_at((x, y))
                if cell:
                    cell.position = (x, y)

class CharacterGrid(GenericGrid):
    """ Each cell is one character, usually ASCII, created from a list of strings """
    def __init__(self, lines: list[str], wrapping = False, default_value = None):
        data: list[list[Cell]] = []
        for y, line in enumerate(lines):
            row = list(map(Cell, list(line)))
            for x, cell in enumerate(row):
                cell.position = (x, y)
            data.append(row)

        super().__init__(data, wrapping, default_value)

    def print(self):
        for row in self.data:
            print(''.join(map(lambda c: c.contents, row)))