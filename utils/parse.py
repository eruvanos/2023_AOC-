from typing import List

from utils.vector import Vec2


def map_from_lines(lines: List[str]):
    """
    Parse lines into a map of Vec2:char.
    """
    parsed = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            parsed[Vec2(x, y)] = c

    return parsed
