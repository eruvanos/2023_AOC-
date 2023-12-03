# fmt: off
import sys
from collections import defaultdict
from itertools import product
from math import prod

sys.path.append("..")


# fmt: on

def part_1(data):
    available_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    result = 0

    for line in data:
        possible = True

        # Game 1: 7 blue, 4 red, 11 green; 2 red, 2 blue, 7 green; 2 red, 13 blue, 8 green; 18 blue, 7 green, 5 red
        game, line = line.split(":")
        game = int(game[5:])

        sets = line.split(";")
        for s in sets:
            cubes: list[str] = s.split(",")

            for cube in cubes:
                amount, color = cube.strip().split(" ")
                if available_cubes[color] < int(amount):
                    possible = False

        if possible:
            result += game

    return result


def part_2(data):
    available_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    result = 0

    for line in data:
        required_cubes = defaultdict(int)

        # Game 1: 7 blue, 4 red, 11 green; 2 red, 2 blue, 7 green; 2 red, 13 blue, 8 green; 18 blue, 7 green, 5 red
        game, line = line.split(":")
        game = int(game[5:])

        sets = line.split(";")
        for s in sets:
            cubes: list[str] = s.split(",")

            for cube in cubes:
                amount, color = cube.strip().split(" ")

                required_cubes[color] = max(required_cubes[color], int(amount))

        result += prod(required_cubes.values())

    return result


def parse(lines):
    # lines = [int(l) for l in lines]
    return lines


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
