# fmt: off
import sys
from itertools import permutations

from utils.parse import map_from_lines
from utils.path import manhattan
from utils.vector import Vec2

sys.path.append("..")


# fmt: on

def part_1(data):
    data = expand(data)
    world = map_from_lines(data)

    galaxies = [pos for pos, c in world.items() if c == "#"]

    result = 0
    for g1, g2 in permutations(galaxies, 2):
        result += manhattan(g1, g2)
    return result // 2


def part_2(data, n=1000000):
    x_ex, y_ex = expanders(data)

    world = map_from_lines(data)
    galaxies = [pos for pos, c in world.items() if c == "#"]

    expanded_world = {}
    for g in galaxies:
        x, y = g

        for ex in x_ex:
            if g.x > ex:
                x += n-1
            else:
                break

        for ex in y_ex:
            if g.y > ex:
                y += n-1
            else:
                break

        expanded_world[Vec2(x, y)] = "#"

    result = 0
    for g1, g2 in permutations(expanded_world, 2):
        result += manhattan(g1, g2)

    return result // 2


def parse(lines):
    # lines = [int(l) for l in lines]
    return lines


def expand(lines):
    expanded = []
    for l in lines:
        expanded.append(l)
        if "#" not in l:
            expanded.append(l)

    # flip lines
    flipped = list(zip(*expanded))
    expanded_2 = []
    for l in flipped:
        expanded_2.append(l)
        if "#" not in l:
            expanded_2.append(l)
    lines = list(zip(*expanded_2))
    return lines

def expanders(lines):
    y_expanders = []
    for y, l in enumerate(lines):
        if "#" not in l:
            y_expanders.append(y)

    flipped = list(zip(*lines))

    x_expanders = []
    for x, l in enumerate(flipped):
        if "#" not in l:
            x_expanders.append(x)

    return x_expanders, y_expanders


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(parse(lines[:])))
    print("Part 2: ", part_2(parse(lines[:])))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
