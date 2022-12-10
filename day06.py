import numpy as np
import re

from collections import defaultdict
from copy import deepcopy
from start_day import AdventOfCodeDay


def find_sequence(s, n):
    i = 0
    buffer = s[:n]
    while len(set(buffer)) != n:
        i += 1
        buffer = s[i : i + n]
    return i + n


if __name__ == "__main__":
    aoc = AdventOfCodeDay(6, overwrite=True)
    data = aoc.load_strings(strip=False)[0]

    print("Solution")
    print("  1.", find_sequence(data, 4))
    print("  2.", find_sequence(data, 14))
