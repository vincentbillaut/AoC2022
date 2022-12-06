import numpy as np
import re
from start_day import AdventOfCodeDay

pattern = re.compile(r"(\d*)-(\d*),(\d*)-(\d*)")


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

    data_parsed = [(int(a), int(b), int(c), int(d)) for a, b, c, d in aoc.load_regex(pattern, 4)]

    print("Solution")
    print("  1.", sum(fully_contained(r) for r in data_parsed))
    print("  2.", sum(overlap(r) for r in data_parsed))
