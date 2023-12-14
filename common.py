from typing import Any, Tuple

def taxicab_distance(from_: Tuple[int, int], to: Tuple[int, int]):
    return abs(from_[0] - to[0]) + abs(from_[1] - to[1])

class GenericGrid:
    def __init__(self, data: list[list[Any]], wrapping = False, default_value: Any = None):
        self.data = list(data)
        self.row_count = len(self.data)
        self.col_count = len(self.data[0]) if len(self.data) > 0 else 0

        # If wrapping = True, accessing one to the right of the rightmost column will wrap to the leftmost column, and so on
        # If wrapping = False, the grid is padded in all directions by infinitely many default_value cells
        self.wrapping = wrapping
        self.default_value = default_value

    def __eq__(self, other):
        if not isinstance(other, GenericGrid):
            return False
        if not (other.row_count == self.row_count and other.col_count == self.col_count):
            return False
        return self.data == other.data

    @classmethod
    def wrap_coordinate(cls, c, max_count):
        """ Transform a coordinate to allow for infinite wrapping, e.g. grid.row(-123) for a 50-row grid """
        if c >= max_count:
            c = c % max_count
        elif c <= -max_count:
            c = c % -max_count
        return c

    def row(self, y) -> list[Any]:
        if y >= 0 and y < self.row_count:
            return self.data[y]
        elif self.wrapping:
            y = GenericGrid.wrap_coordinate(y, self.row_count)
            return self.data[y]
        else:
            return [None] * self.col_count

    def col(self, x) -> list[Any]:
        if x >= 0 and x < self.col_count:
            return [self.data[y][x] for y in range(self.row_count)]
        elif self.wrapping:
            x = GenericGrid.wrap_coordinate(x, self.col_count)
            return [self.data[y][x] for y in range(self.row_count)]
        else:
            return [None] * self.row_count

    def rows(self) -> list[list[Any]]:
        return self.data

    def cols(self) -> list[list[Any]]:
        return [list(x) for x in zip(*self.data)]

    def transpose(self):
        self.data = self.cols()
        self.row_count = len(self.data)
        self.col_count = len(self.data[0]) if len(self.data) > 0 else 0

    def flip_horizontal(self):
        for y in range(self.row_count):
            self.data[y] = list(reversed(self.data[y]))

    def flip_vertical(self):
        for x in range(self.col_count):
            rev = reversed(self.col(x))
            for y, c in enumerate(rev):
                self.data[y][x] = c

    def rotate(self):
        """ Rotate the grid 90 degrees, clockwise. """
        self.transpose()
        self.flip_horizontal()

    def cell_at(self, position: Tuple[int, int]):
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

    def neighbor_coordinates(self, position: Tuple[int, int], include_diagonals=True) -> list[Tuple[int, int]]:
        coordinate_pairs = []
        (x, y) = position
        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                if not include_diagonals and abs(offset_x) == 1 and abs(offset_y) == 1:
                    continue
                coordinate_pairs.append((x + offset_x, y + offset_y))

        assert(len(coordinate_pairs) == 8 if include_diagonals else 4)
        return coordinate_pairs

    def neighbors(self, position: Tuple[int, int], include_diagonals=True) -> list[Any]:
        """ Return a list of all neighboring cells, wrapping or inserting default valued cells if needed. """
        return [self.cell_at(coordinate_pair) for coordinate_pair in self.neighbor_coordinates(position, include_diagonals)]

    def insert_row(self, before_row, new_cells):
        assert(self.row_count >= before_row)
        assert(len(new_cells) == self.col_count)
        self.data.insert(before_row, new_cells)
        self.row_count += 1

    def insert_col(self, before_col, new_cells):
        assert(self.col_count >= before_col)
        assert(len(new_cells) == self.row_count)

        for y in range(self.row_count):
            self.data[y].insert(before_col, new_cells[y])

        self.col_count += 1

class CharacterGrid(GenericGrid):
    """ Each cell is one character, usually ASCII, created from a list of strings """
    def __init__(self, lines: list[str], wrapping = False, default_value = None):
        data = [list(line) for line in lines]
        super().__init__(data, wrapping, default_value)

    def print(self):
        print(self.dump())

    def dump(self):
        return '\n'.join([''.join(row) for row in self.data])