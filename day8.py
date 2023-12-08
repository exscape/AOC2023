import re
import itertools
from math import lcm

def parse_network(net):
    NODE_REGEX = re.compile(r'(\w+) = \((\w+), (\w+)\)')
    network = {}

    for line in net:
        node, left, right = NODE_REGEX.match(line).groups() # type: ignore
        network[node] = (left, right)

    return network

# Part 1
def count_steps(directions, network):
    current_node = 'AAA'

    for step, dir in enumerate(itertools.chain.from_iterable(itertools.repeat(directions)), start=1):
        index = 0 if dir == 'L' else 1
        current_node = network[current_node][index]
        if current_node == 'ZZZ':
            return step

# Part 2
def count_steps_simultaneous(directions, network):
    current_nodes = [k for k in network.keys() if k.endswith("A")]
    cycle_length = [0] * len(current_nodes)

    for step, dir in enumerate(itertools.chain.from_iterable(itertools.repeat(directions)), start=1):
        index = 0 if dir == 'L' else 1
        for i, node in enumerate(current_nodes):
            current_nodes[i] = network[node][index]

            if current_nodes[i].endswith("Z"):
                cycle_length[i] = step

        if all([n > 0 for n in cycle_length]):
            break

    return lcm(*cycle_length)

if __name__=='__main__':
    lines = open('data/day8.txt').read().splitlines()
    directions = lines[0]
    network = parse_network(lines[2:])

    print(f"Part 1: {count_steps(directions, network)}")
    print(f"Part 2: {count_steps_simultaneous(directions, network)}")