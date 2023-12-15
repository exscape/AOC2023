from collections import namedtuple

Lens = namedtuple('Lens', ['label', 'focal_length'])

def hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val

def solve(steps):
    # Part 1
    init_sequence_sum = sum(hash(step) for step in steps)

    # Part 2
    boxes = [[] for _ in range(256)]
    for step in steps:
        if '=' in step:
            label, focal_length = step.split('=')
            box = hash(label)
            new_lens = Lens(label, int(focal_length))

            for i, lens in enumerate(boxes[box]):
                if lens.label == new_lens.label:
                    boxes[box][i] = new_lens
                    break
            else:
                boxes[box].append(new_lens)
        elif '-' in step:
            label = step[:-1]
            box = hash(label)
            boxes[box] = [lens for lens in boxes[box] if lens.label != label]

    focusing_power = 0
    for box_id, box in enumerate(boxes, start=1):
        for lens_id, lens in enumerate(box, start=1):
            focusing_power += box_id * lens_id * lens.focal_length

    return (init_sequence_sum, focusing_power)

if __name__=='__main__':
    steps = open('data/day15.txt').read().replace('\n', '').split(',')
    part1, part2 = solve(steps)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")