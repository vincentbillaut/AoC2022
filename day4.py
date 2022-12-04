import numpy as np
import re
from start_day import AdventOfCodeDay

pattern = re.compile(r"(\d*)-(\d*),(\d*)-(\d*)")


def parse_row(row):
    match = re.match(pattern, row)
    return int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))


def fully_contained(r):
    a, b, c, d = r
    if a <= c and d <= b:
        return True
    if c <= a and b <= d:
        return True
    return False


def overlap(r):
    a, b, c, d = r
    return a <= c <= b or c <= a <= d


if __name__ == "__main__":
    aoc = AdventOfCodeDay(4, overwrite=True)
    data = aoc.load_strings()

    data_parsed = [parse_row(r) for r in data]

    print("Solution")
    print("  1.", sum(fully_contained(r) for r in data_parsed))
    print("  2.", sum(overlap(r) for r in data_parsed))
