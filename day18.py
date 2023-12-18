# pyright: reportOptionalMemberAccess=false
import re
import itertools

class Dig:
    dir: str
    length: int

    def __init__(self, dir, length):
        self.dir = dir
        self.length = int(length)

def calculate_num_blocks(digs):
    # Generate a list of vertices for the polygon
    (x, y) = (0, 0)
    vertices = [(0, 0)]
    for dig in digs:
        match dig.dir:
            case 'L': x -= dig.length
            case 'R': x += dig.length
            case 'U': y -= dig.length
            case 'D': y += dig.length
        vertices.append((x, y))

    # Triangle formula, related to the Shoelace formula
    area = 0.5 * abs(sum( (a[1] + b[1]) * (a[0] - b[0]) for a, b in itertools.pairwise(vertices) ))

    # Pick's Theorem: "Pick's theorem provides a formula for the area of a simple polygon with integer vertex coordinates, in terms of the number of integer points within it and on its boundary"
    # Area of polygon = # interior points + (boundary points)/2 - 1
    # We know the area (above), and want the total number of points (internal and boundary), so solve the equation for i + b:
    # A = i + b/2 - 1 ==> i = A - b/2 + 1 ==> i + b = A + b/2 + 1
    b = sum(dig.length for dig in digs)
    return int(area + b/2 + 1)

if __name__=='__main__':
    lines = open('data/day18.txt').read().splitlines()
    dig_regex = re.compile(r'(\w) (\d+)')
    color_regex = re.compile(r'#([0-9a-fA-F]{6})')
    digs_part1 = [Dig(*re.match(dig_regex, line).groups()) for line in lines]

    digs_part2 = []
    colors = color_regex.findall('\n'.join(lines))
    dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    for color in colors:
        dir = dir_map[color[-1]]
        length = int(color[:5], base=16)
        digs_part2.append(Dig(dir, length))

    print(f"Part 1: {calculate_num_blocks(digs_part1)}")
    print(f"Part 2: {calculate_num_blocks(digs_part2)}")