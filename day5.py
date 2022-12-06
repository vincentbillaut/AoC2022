import numpy as np
import re

from collections import defaultdict
from copy import deepcopy
from start_day import AdventOfCodeDay


move_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)*")


def get_crates(data):
    i = 0
    crates = defaultdict(list)
    while "[" in data[i]:
        for crate_n in range(9):
            label = data[i][1 + 4 * crate_n]
            if label != " ":
                crates[crate_n + 1].append(label)
        i += 1
    return crates


def apply_moves(orig_crates, moves):
    crates = deepcopy(orig_crates)
    for n, from_crate, to_crate in moves:
        for i in range(n):
            content = crates[from_crate].pop()
            crates[to_crate].append(content)
    return crates


def apply_moves_9001(orig_crates, moves):
    crates = deepcopy(orig_crates)
    for n, from_crate, to_crate in moves:
        content = crates[from_crate][-n:]
        crates[from_crate] = crates[from_crate][:-n]
        crates[to_crate].extend(content)
    return crates


top_crates_str = lambda crates: "".join(crates[i + 1][-1] for i in range(9))

if __name__ == "__main__":
    aoc = AdventOfCodeDay(5, overwrite=True)
    data = aoc.load_strings(strip=False)

    reversed_crates = get_crates(data)
    moves = [(int(a), int(b), int(c)) for a, b, c in aoc.load_regex(move_pattern, 3)]

    # reverse crates
    crates = {}
    for k in reversed_crates:
        crates[k] = reversed_crates[k][::-1]

    result_crates = apply_moves(crates, moves)
    result_crates2 = apply_moves_9001(crates, moves)

    print("Solution")
    print("  1.", top_crates_str(result_crates))
    print("  2.", top_crates_str(result_crates2))
