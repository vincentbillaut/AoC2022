import math
from collections import defaultdict
from start_day import AdventOfCodeDay

DIRECTIONS = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
neighbors = lambda x, y: {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (x, y)}


def parse_lines(line_data):
    start = ([i for i, c in enumerate(line_data[0]) if c != "#"][0], 0)
    end = ([i for i, c in enumerate(line_data[-1]) if c != "#"][0], len(line_data) - 1)
    data, walls = defaultdict(list), {(start[0], start[1] - 1), (end[0], end[1] + 1)}
    for j, l in enumerate(line_data):
        data.update({(i, j): [c] for i, c in enumerate(l) if c != "#"})
        walls = walls | {(i, j) for i, c in enumerate(l) if c == "#"}
    return start, end, data, walls


def blizzard_step(data, walls):
    new_data = defaultdict(list)
    min_j, max_j = min(y for x, y in data), max(y for x, y in data)
    min_i, max_i = min(x for x, y in data), max(x for x, y in data)

    def new_location(pt, blizz):
        vec = DIRECTIONS[blizz]
        proposed_pt = (pt[0] + vec[0], pt[1] + vec[1])
        if proposed_pt not in walls:
            return proposed_pt
        if blizz == ">":
            return (min_i, pt[1])
        if blizz == "<":
            return (max_i, pt[1])
        if blizz == "^":
            return (pt[0], max_j - 1)  # end   is at max_j
        if blizz == "v":
            return (pt[0], min_j + 1)  # start is at min_j

    for pt in data:
        for blizz in data[pt]:
            if blizz != ".":
                new_data[new_location(pt, blizz)].append(blizz)
    for pt in data:
        if pt not in new_data:
            new_data[pt].append(".")
    return new_data


def trip(start, end, data, walls, back_and_forth=False):
    n_rows, n_cols = len(set(x for (x, y) in data)) - 2, len(set(x for (x, y) in data))
    period = math.lcm(n_rows, n_cols)
    all_data = [data.copy()]

    def _shortest_path_bfs(start, end, offset=0):
        bfs_set, t = {start}, offset
        while end not in bfs_set:
            new_set, t = set(), t + 1
            if (t % period) >= len(all_data):
                all_data.append(blizzard_step(all_data[-1], walls))
                assert t % period < len(all_data)
            for node in bfs_set:
                in_map_options = neighbors(*node) - walls
                new_set = new_set | {option for option in in_map_options if all_data[t % period][option][0] == "."}
            bfs_set = new_set
        return t

    first = _shortest_path_bfs(start, end)
    print("  1.", first)
    if not back_and_forth:
        return first
    second = _shortest_path_bfs(end, start, offset=first)
    third = _shortest_path_bfs(start, end, offset=second)
    print("  2.", third)
    return third


if __name__ == "__main__":
    aoc = AdventOfCodeDay(24, overwrite=False, display=False)
    data = parse_lines(aoc.load_strings())

    print("Solution")
    trip(*data, back_and_forth=True)
