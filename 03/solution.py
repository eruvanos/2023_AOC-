# fmt: off
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List

sys.path.append("..")


# fmt: on

@dataclass
class Number:
    value: int
    line: int
    start: int
    end: int


def part_1(data):
    # based on: https://jeff.glass/post/advent-of-code-2023/

    symbols = set()  # x,y coordinates of symbols
    part_numbers = []

    number_pattern = re.compile("(\d+)")
    symbol_pattern = re.compile("([^\d.])")

    for r, row in enumerate(data):

        for s in re.finditer(symbol_pattern, row):
            symbols.add((s.start(), r))

        for n in re.finditer(number_pattern, row):
            part_numbers.append(Number(
                value=int(n.group()),
                line=r,
                start=n.start(),
                end=n.end()
            ))

    result = 0
    for number in part_numbers:
        if (number.start - 1, number.line) in symbols or (number.end, number.line) in symbols:
            result += number.value
            continue

        for x in range(number.start - 1, number.end + 1):
            if (x, number.line - 1) in symbols or (x, number.line + 1) in symbols:
                result += number.value
                break

    return result


def part_2(data):
    symbols = set()  # x,y coordinates of symbols
    part_numbers = []

    gears = defaultdict(list)  # gear -> numbers

    number_pattern = re.compile("(\d+)")
    symbol_pattern = re.compile("(\*)")

    for r, row in enumerate(data):

        for s in re.finditer(symbol_pattern, row):
            symbols.add((s.start(), r))

        for n in re.finditer(number_pattern, row):
            part_numbers.append(Number(
                value=int(n.group()),
                line=r,
                start=n.start(),
                end=n.end()
            ))

    for number in part_numbers:
        if (number.start - 1, number.line) in symbols:
            gears[(number.start - 1, number.line)].append(number)
            continue

        if (number.end, number.line) in symbols:
            gears[(number.end, number.line)].append(number)
            continue

        for x in range(number.start - 1, number.end + 1):
            if (x, number.line - 1) in symbols:
                gears[(x, number.line - 1)].append(number)
                break

            if (x, number.line + 1) in symbols:
                gears[(x, number.line + 1)].append(number)
                break

    result = 0
    for gear, numbers in gears.items():
        if len(numbers) == 2:
            g1, g2 = numbers
            result += g1.value * g2.value

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
