from enum import Enum
from common import CharacterGrid

class Dir(Enum):
    N = (0, -1)
    S = (0, 1)
    W = (-1, 0)
    E = (1, 0)

def follow_beam(grid, starting_state, visited = None, depth = 0):
    visited = visited or set()
    x, y, dir = starting_state

    while (x, y, dir) not in visited and 0 <= x < grid.col_count and 0 <= y < grid.row_count:
        visited.add((x, y, dir))

        match grid.cell_at((x,y)):
            case '/':
                # Flip the direction: N => E, S => W, E => N, W => S
                dir = Dir((-dir.value[1], -dir.value[0]))
            case '\\':
                # Flip the direction: N => W, S => E, E => S, W => N
                dir = Dir((dir.value[1], dir.value[0]))
            case '-' if dir in (Dir.N, Dir.S):
                # Split into two beams, going east and west
                follow_beam(grid, (x, y, Dir.W), visited, depth + 1)
                dir = Dir.E
            case '|' if dir in (Dir.E, Dir.W):
                # Split into two beams, going north and south
                follow_beam(grid, (x, y, Dir.N), visited, depth + 1)
                dir = Dir.S
            case _:
                pass # Keep on moving in the same direction

        x += dir.value[0]
        y += dir.value[1]

    # Speeds things up by a factor of 22 versus always counting
    if depth == 0:
        energized = {(x, y) for (x, y, _) in visited}
        return len(energized)
    else:
        return 0

def solve(lines):
    grid = CharacterGrid(lines, wrapping=False, default_value='.')
    state = (0, 0, Dir.E)
    part1 = follow_beam(grid, state)

    starts = [(x, 0, Dir.S) for x in range(grid.col_count)]
    starts += [(x, grid.row_count - 1, Dir.N) for x in range(grid.col_count)]
    starts += [(0, y, Dir.E) for y in range(grid.row_count)]
    starts += [(grid.col_count - 1, y, Dir.W) for y in range(grid.row_count)]
    part2 = max(follow_beam(grid, s) for s in starts)

    return (part1, part2)

if __name__=='__main__':
    lines = open('data/day16.txt').read().splitlines()
    part1, part2 = solve(lines)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")