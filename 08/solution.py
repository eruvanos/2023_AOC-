# fmt: off
import sys
from itertools import cycle, count
from math import lcm

sys.path.append("..")


# fmt: on

def part_1(data):
    instructions = cycle(data.pop(0))

    _ = data.pop(0)

    world = dict()

    for line in data:
        # BBB = (DDD, EEE)
        loc = line[0:3]
        left = line[7:10]
        right = line[12:15]

        world[loc] = (left, right)

    current = "AAA"

    for i, d in enumerate(instructions):
        left, right = world[current]

        if d == "L":
            current = left
        elif d == "R":
            current = right
        else:
            raise ValueError("Unknown direction")

        if current == "ZZZ":
            return i + 1


def walk(start, inst, world):
    current = start

    for d in cycle(inst):
        left, right = world[current]

        if d == "L":
            current = left
        elif d == "R":
            current = right
        else:
            raise ValueError("Unknown direction")

        yield current


def part_2(data):
    instructions = data.pop(0)
    _ = data.pop(0)
    world = dict()
    for line in data:
        loc = line[0:3]
        left = line[7:10]
        right = line[12:15]

        world[loc] = (left, right)

    runner = [walk(k, instructions, world) for k in world.keys() if k.endswith("A")]

    intergers = []

    for r in runner:
        for i in count(1):
            current = next(r)
            if current.endswith("Z"):
                intergers.append(i)
                break

    return lcm(*intergers)


def parse(lines):
    # lines = [int(l) for l in lines]
    return lines


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(parse(lines[:])))
    print("Part 2: ", part_2(parse(lines[:])))
    # falsch: 145288587985807687534080


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
