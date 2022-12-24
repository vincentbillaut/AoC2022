from collections import Counter
from itertools import product
from start_day import AdventOfCodeDay

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def build_elfs(line_data):
    s = set()
    for j, l in enumerate(line_data):
        s = s | set((i, j) for i, c in enumerate(l) if c == "#")
    return s


def count_empty_space(elfs):
    t, min_x, min_y = 0, min(x for x, y in elfs), min(y for x, y in elfs)
    max_x, max_y = max(x for x, y in elfs), max(y for x, y in elfs)
    return sum(sum(((i, j) not in elfs) for i in range(min_x, max_x + 1)) for j in range(min_y, max_y + 1))


def neighbors(elf, direction=None):
    elfx, elfy = elf
    if direction is None:
        return set(product([elfx - 1, elfx, elfx + 1], [elfy - 1, elfy, elfy + 1])) - {(elfx, elfy)}
    if direction[0] == 0:
        return set(product([elfx - 1, elfx, elfx + 1], [elfy + direction[1]]))
    return set(product([elfx + direction[0]], [elfy - 1, elfy, elfy + 1]))


def propose_move(elf, elfs, facing):
    directions_to_try = [DIRECTIONS[(facing + i) % 4] for i in range(4)]

    def _propose_move(directions):
        if len(directions) == 0:
            return None
        direction = directions[0]
        directional_neighbors = neighbors(elf, direction)
        if elfs & directional_neighbors:
            return _propose_move(directions[1:])
        return (elf[0] + direction[0], elf[1] + direction[1])

    return _propose_move(directions_to_try)


def step(elfs, start_facing):
    changed = False
    to_move = {elf for elf in elfs if len(elfs & neighbors(elf)) > 0}
    new_elfs = elfs - to_move
    proposed_moves = {}
    for elf in to_move:
        proposed_move = propose_move(elf, elfs, start_facing)
        if proposed_move is not None:
            proposed_moves[elf] = proposed_move
        else:
            new_elfs.add(elf)
    counts = Counter(proposed_moves.values())
    for elf, new_pos in proposed_moves.items():
        if counts[new_pos] == 1:
            new_elfs.add(new_pos)
            changed = True
        else:
            new_elfs.add(elf)
    return new_elfs, changed


def simulate(inp, n=-1):
    elfs, start_facing, i = build_elfs(inp), 0, 0
    elfs, changed = step(elfs, start_facing)
    while changed:
        start_facing, i = (start_facing + 1) % 4, i + 1
        if i == n:
            return count_empty_space(elfs)
        elfs, changed = step(elfs, start_facing)
    return i + 1


if __name__ == "__main__":
    aoc = AdventOfCodeDay(23, overwrite=False, display=False)
    data = aoc.load_strings()

    print("Solution")
    print("  1.", simulate(data, 10))
    print("  2.", simulate(data))
