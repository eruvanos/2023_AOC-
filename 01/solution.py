# fmt: off
import sys

sys.path.append("..")


# fmt: on

NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
R_NUMBERS = list(map(lambda n: ''.join(reversed(n)), NUMBERS))

def part_1(data):

    sum = 0
    for l in data:
        for s in l:
            if s.isnumeric():
                first = s
                break
        for s in reversed(l):
            if s.isnumeric():
                last = s
                break

        sum += int(first + last)

    return sum

def first_number(l):
    for i in range(len(l)):
        s = l[i]
        if s.isnumeric():
            return s
        else:
            for k, n in enumerate(NUMBERS, 1):
                if l[i:].startswith(n):
                    return str(k)

    return None

def last_number(l):
    lr = "".join(reversed(l))
    for i in range(len(lr)):
        s = lr[i]
        if s.isnumeric():
            return s
        else:
            for k, n in enumerate(R_NUMBERS, 1):
                if lr[i:].startswith(n):
                    return str(k)

def part_2(data):
    # sumitted
    # sum = 0
    # for l in data:
    #
    #     first = first_number(l)
    #     last = last_number(l)
    #
    #     assert first is not None
    #     assert last is not None
    #
    #     sum += int(first + last)
    #
    # return sum

    # refactored with new idea
    sum = 0
    for l in data:

        for i, n in enumerate(NUMBERS, 1):
            l = l.replace(n, n[0] + str(i) + n[-1])

        for s in l:
            if s.isnumeric():
                first = s
                break
        for s in reversed(l):
            if s.isnumeric():
                last = s
                break

        sum += int(first + last)

    return sum


def parse(lines):
    # lines = [convertparse_line(l) for l in lines]
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
