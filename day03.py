import numpy as np
from start_day import AdventOfCodeDay


value = lambda item: ord(item) - (96 if item in "qwertyuiopasdfghjklzxcvbnm" else 38)


def parse_rucksack(r):
    n = len(r)
    left, right = r[: n // 2], r[n // 2 :]
    inters = set(left) & set(right)
    item = inters.pop()
    return value(item)


def parse_set(r1, r2, r3):
    inters = set(r1) & set(r2) & set(r3)
    badge = inters.pop()
    return value(badge)


if __name__ == "__main__":
    aoc = AdventOfCodeDay(3)
    data = aoc.load_strings()

    print("Solution")
    print("  1.", sum([parse_rucksack(r) for r in data]))
    print("  2.", sum([parse_set(data[3 * i], data[3 * i + 1], data[3 * i + 2]) for i in range(len(data) // 3)]))
