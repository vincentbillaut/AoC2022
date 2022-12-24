import re
import sys
from start_day import AdventOfCodeDay

sys.setrecursionlimit(12000)

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
FACE = {(1, 0): "A", (2, 0): "B", (1, 1): "C", (0, 2): "D", (1, 2): "E", (0, 3): "F"}
MOVES = {
    "A": {
        (-1, 0): lambda x, y: ((0, 100 + (49 - y)), 0),  # A --> D
        (0, -1): lambda x, y: ((0, 150 + (x - 50)), 0),  # A --> F
    },
    "B": {
        (1, 0): lambda x, y: ((99, 149 - y), 2),  # B --> E
        (0, 1): lambda x, y: ((99, 50 + (x - 100)), 2),  # B --> C
        (0, -1): lambda x, y: ((x - 100, 199), 3),  # B --> F
    },
    "C": {
        (1, 0): lambda x, y: ((100 + (y - 50), 49), 3),  # C --> B
        (-1, 0): lambda x, y: ((y - 50, 100), 1),  # C --> D
    },
    "D": {
        (-1, 0): lambda x, y: ((50, 149 - y), 0),  # D --> A
        (0, -1): lambda x, y: ((50, x + 50), 0),  # D --> C
    },
    "E": {
        (1, 0): lambda x, y: ((149, 149 - y), 2),  # E --> B
        (0, 1): lambda x, y: ((49, 150 + (x - 50)), 2),  # E --> F
    },
    "F": {
        (1, 0): lambda x, y: ((50 + (y - 150), 149), 3),  # F --> E
        (0, 1): lambda x, y: ((x + 100, 0), 1),  # F --> B
        (-1, 0): lambda x, y: ((50 + (y - 150), 0), 1),  # F --> A
    },
}


def basic_move_proposal(current, facing, spaces, walls):
    direction = DIRECTIONS[facing]
    min_y_of_col, max_y_of_col = min(y for x, y in spaces | walls if x == current[0]), max(
        y for x, y in spaces | walls if x == current[0]
    )
    min_x_of_row, max_x_of_row = min(x for x, y in spaces | walls if y == current[1]), max(
        x for x, y in spaces | walls if y == current[1]
    )
    new_pos_y = current[1] if direction[1] == 0 else (min_y_of_col if current[1] == max_y_of_col else max_y_of_col)
    new_pos_x = current[0] if direction[0] == 0 else (min_x_of_row if current[0] == max_x_of_row else max_x_of_row)
    return (new_pos_x, new_pos_y), facing


def cubic_move_proposal(current, facing, spaces=None, walls=None):
    direction = DIRECTIONS[facing]
    face = FACE[(current[0] // 50, current[1] // 50)]
    new_pos, new_facing = MOVES[face][direction](*current)
    return new_pos, new_facing


def universal_move(move_proposal):
    def _univ_move(current, facing, spaces, walls):
        direction = DIRECTIONS[facing]
        new_pos = (current[0] + direction[0], current[1] + direction[1])
        if new_pos in spaces:
            return new_pos, facing
        if new_pos in walls:
            return current, facing
        new_pos, new_facing = move_proposal(current, facing, spaces, walls)
        if new_pos in walls:
            return current, facing
        return new_pos, new_facing

    return _univ_move


def parse_input(line_data):
    free_spaces, walls = set(), set()
    for j in range(len(line_data)):
        if line_data[j] == "":
            break
        free_spaces = free_spaces | {(i, j) for i, c in enumerate(line_data[j]) if c == "."}
        walls = walls | {(i, j) for i, c in enumerate(line_data[j]) if c == "#"}
    return free_spaces, walls, line_data[j + 1]


def final_point(inp, move_function):
    free_spaces, walls, inp_instructions = parse_input(inp)
    starting_point, direction_i = (min(x for x, y in free_spaces if y == 0), 0), 0

    def process_instructions(current, facing, instructions):
        if instructions == "":
            return current, facing
        if instructions[0] in "RL":
            new_facing = (facing - 1 + 2 * int(instructions[0] == "R")) % 4
            return process_instructions(current, new_facing, instructions[1:])
        match = re.match(r"^(\d+)", instructions)
        distance, end = int(match.group(1)), match.end()
        for _ in range(distance):
            current, facing = move_function(current, facing, free_spaces, walls)
        return process_instructions(current, facing, instructions[end:])

    final_point, final_facing = process_instructions(starting_point, direction_i, inp_instructions)
    return 1000 * (final_point[1] + 1) + 4 * (final_point[0] + 1) + final_facing


if __name__ == "__main__":
    aoc = AdventOfCodeDay(22, overwrite=False, display=False)
    data = [x.split("\n")[0] for x in aoc.load_strings(strip=False)]

    print("Solution")
    print("  1.", final_point(data, universal_move(basic_move_proposal)))
    print("  2.", final_point(data, universal_move(cubic_move_proposal)))
