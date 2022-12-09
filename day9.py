import numpy as np
import re
from start_day import AdventOfCodeDay


def move(pos, direction):
    x, y = pos
    match direction:
        case "U":
            return x, y + 1
        case "D":
            return x, y - 1
        case "L":
            return x - 1, y
        case "R":
            return x + 1, y


def new_tail(head, tail):
    hx, hy = head
    tx, ty = tail
    if max(abs(hx - tx), abs(hy - ty)) <= 1:
        return tail  # they touch
    return tx + int(np.sign(hx - tx)), ty + int(np.sign(hy - ty))


def new_positions(head, positions, size):
    target = head
    for i in range(1, size):
        positions[i] = new_tail(target, positions[i])
        target = positions[i]
    return positions


def n_visited(instructions, size):
    head = (0, 0)
    positions = {}
    for i in range(1, size):
        positions[i] = (0, 0)
    visited_tail = {positions[size - 1]}
    for direction, n in instructions:
        for _ in range(n):
            head = move(head, direction)
            positions = new_positions(head, positions, size)
            visited_tail.add(positions[size - 1])
    return len(visited_tail)


if __name__ == "__main__":
    aoc = AdventOfCodeDay(9, overwrite=True)
    data_string = aoc.load_regex(re.compile(r"(U|D|L|R) (\d+)"), 2)
    data = [(a, int(b)) for a, b in data_string]

    print("Solution")
    print("  1.", n_visited(data, 2))
    print("  2.", n_visited(data, 10))
