import math
import networkx as nx
import numpy as np
import re

from collections import defaultdict
from copy import deepcopy
from itertools import product
from tqdm import tqdm_notebook

from start_day import AdventOfCodeDay


def initialize(data):
    occupied = set()
    for line in data:
        for i in range(len(line) - 1):
            (x, y), (tx, ty) = line[i], line[i + 1]
            while x != tx or y != ty:
                occupied.add((x, y))
                x, y = x + int(np.sign(tx - x)), y + int(np.sign(ty - y))
        occupied.add((tx, ty))
    return occupied


def move_sand_down(x, y, occupied_dict, max_depth, is_floor):
    if (x, y) in occupied_dict or (y > max_depth and not is_floor):
        return False, None
    if y == max_depth - 1 and is_floor:
        return True, (x, y)
    if (x, y + 1) not in occupied_dict:
        return move_sand_down(x, y + 1, occupied_dict, max_depth, is_floor)
    if (x - 1, y + 1) not in occupied_dict:
        return move_sand_down(x - 1, y + 1, occupied_dict, max_depth, is_floor)
    if (x + 1, y + 1) not in occupied_dict:
        return move_sand_down(x + 1, y + 1, occupied_dict, max_depth, is_floor)
    return True, (x, y)


def sand_falling(source, init_occupied_dict, floor_allowed):
    occupied_dict, count, max_depth = init_occupied_dict.copy(), 0
    max_depth = max(y for _, y in occupied_dict) + 2 * int(floor_allowed)
    at_rest, pos = move_sand_down_test(source[0], source[1], occupied_dict, max_depth, floor_allowed)
    while at_rest and source not in occupied_dict:
        occupied_dict.add(pos)
        count += 1
        at_rest, pos = move_sand_down_test(source[0], source[1], occupied_dict, max_depth, floor_allowed)
    return count


if __name__ == "__main__":
    aoc = AdventOfCodeDay(14, overwrite=True)
    data = [[(int(x.split(",")[0]), int(x.split(",")[1])) for x in l.split(" -> ")] for l in aoc.load_strings()]
    initially_occupied = initialize(data)

    print("Solution")
    print("  1.", sand_falling((500, 0), initially_occupied, floor_allowed=False))
    print("  2.", sand_falling((500, 0), initially_occupied, floor_allowed=True))
