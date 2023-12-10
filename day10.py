from enum import IntFlag
from common import GenericGrid, Cell

class Dir(IntFlag):
    EMPTY = 0
    N = 1
    W = 2
    E = 4
    S = 8
    VERT = N | S
    HOR  = W | E
    NE   = N | E
    NW   = N | W
    SW   = S | W
    SE   = S | E

    def opposite(self):
        assert(self in [self.N, self.S, self.W , self.E])
        if self == self.N: return self.S
        if self == self.S: return self.N
        if self == self.W: return self.E
        if self == self.E: return self.W

    @classmethod
    def from_char(cls, ch):
        return {'|': cls.VERT, '-': cls.HOR, 'L': cls.NE, 'J': cls.NW, '7': cls.SW, 'F': cls.SE, 'S': cls.EMPTY, '.': cls.EMPTY}[ch]

    def to_char(self):
        return {self.VERT: '|', self.HOR: '-', self.NE: 'L', self.NW: 'J', self.SW: '7', self.SE: 'F', self.EMPTY: '.'}[self]

class Pipe:
    def __init__(self, ch):
        self.ch = ch
        self.dirs = Dir.from_char(ch)

    def connects(self, other_dir):
        """ Does this pipe allow movement in the direction other_dir? """
        return bool(self.dirs & other_dir)

    def __repr__(self):
        return self.ch

def next_dir(pipe_dirs, last_dir):
    """ When we reach a new pipe, the direction to go is the one of its allowed directions that we did NOT come from """
    return [d for d in list(pipe_dirs) if d != last_dir.opposite()][0]

def next_pos(position, dir):
    """ Given a position and a direction to follow, where would we end up? """
    offset_x = 0
    offset_y = 0
    assert(dir in [Dir.N, Dir.S, Dir.W, Dir.E])
    if dir == Dir.N: offset_y = -1
    elif dir == Dir.S: offset_y = 1
    elif dir == Dir.W: offset_x = -1
    elif dir == Dir.E: offset_x = 1

    (x, y) = position
    return (x + offset_x, y + offset_y)

class PipeGrid(GenericGrid):
    def __init__(self, lines, wrapping=False, default_value=None):
        self._start_coordinates = None

        # Parse the data and create the grid
        data = []
        for y, line in enumerate(lines):
            row = []
            for x, ch in enumerate(line):
                row.append(Cell(Pipe(ch), (x, y)))
                if ch == 'S':
                    self._start_coordinates = (x, y)
            data.append(row)

        super().__init__(data, wrapping, default_value)

        # Figure out the actual type of pipe at the starting location (S) based on the neighboring pipes
        my_directions = Dir.EMPTY
        (N, W, E, S) = [cell.contents if cell else None for cell in self.neighbors(self.start_coordinates(), include_diagonals=False)]
        if N and N.connects(Dir.S): my_directions |= Dir.N
        if S and S.connects(Dir.N): my_directions |= Dir.S
        if E and E.connects(Dir.W): my_directions |= Dir.E
        if W and W.connects(Dir.E): my_directions |= Dir.W

        # Finally, overwrite the S with a pipe of the correct type
        self.cell_at(self.start_coordinates()).contents = Pipe(my_directions.to_char()) # type: ignore

    def dirs_at(self, position):
        """ Which directions are allowed for the pipe at the given position? """
        return self.cell_at(position).contents.dirs # type: ignore

    def start_coordinates(self):
        assert(self._start_coordinates is not None)
        return self._start_coordinates

    def most_steps(self):
        """ Count the steps along the entire pipe network, and calculate the furthest distance from that """

        # Pick a direction at random; it doesn't matter
        pos = self.start_coordinates()
        outgoing_dir = list(self.dirs_at(pos))[0]
        steps = 0

        while True: # Poor man's do-while loop (I really wish Python implemented them)
            pos = next_pos(pos, outgoing_dir)
            last_dir = outgoing_dir
            outgoing_dir = next_dir(self.dirs_at(pos), last_dir)
            steps += 1
            if pos == self.start_coordinates():
                return steps // 2

def solve(lines):
    grid = PipeGrid(lines, wrapping=False, default_value=None)
    return grid.most_steps()

if __name__=='__main__':
    main_problem = open('data/day10.txt').read()
    lines = main_problem.splitlines()
    print(f"Part 1: {solve(lines)}")