from start_day import AdventOfCodeDay


height = lambda tower: 0 if len(tower) == 0 else (max(y for _, y in tower) + 1)
jet_gas = {"<": (-1, 0), ">": (1, 0)}
shapes = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


def add_shape(tower, shape, instructions, t):
    h = height(tower)
    moving_shape, side = shift_shape(shape, (2, h + 3), tower), True
    while not moving_shape & tower and min(y for _, y in moving_shape) >= 0:
        move = jet_gas[instructions[t]] if side else (0, -1)
        moving_shape = shift_shape(moving_shape, move, tower)
        t = (t + 1) % len(instructions) if side else t
        side = not side
    new_tower = tower | shift_shape(moving_shape, (-move[0], -move[1]), tower)
    return new_tower, t


def shift_shape(shape, direction, tower):
    if direction[0] == -1 and min(x for x, _ in shape) == 0:
        return shape
    if direction[0] == 1 and max(x for x, _ in shape) == 6:
        return shape
    new_shape = {(a + direction[0], b + direction[1]) for a, b in shape}
    if direction[1] == 0 and new_shape & tower:
        return shape
    return new_shape


def clip_tower(tower):
    min_accessible_height = min(max((y for x, y in tower if x == x_coord), default=0) for x_coord in range(7))
    min_accessible_height = max(min_accessible_height - 3, 0)  # not sure why lol
    new_tower = set((x, y - min_accessible_height) for x, y in tower if y >= min_accessible_height)
    assert height(new_tower) + min_accessible_height == height(tower)
    return new_tower, min_accessible_height


def total_height(instructions, n, shapes, debug=False):
    tower, t, cumulated_height = set(), 0, 0
    for i in range(n):
        tower, t = add_shape(tower, shapes[i % len(shapes)], instructions, t)
        tower, h = clip_tower(tower)
        cumulated_height += h
    return cumulated_height + height(tower)


def find_period_in_list(l, repetitions=3):
    for period in range(1, len(l) // repetitions):
        period_checks_out = True
        for rep in range(1, repetitions):
            period_checks_out &= all(l[j] == l[j + rep * period] for j in range(period))
        if period_checks_out:
            return period
    return None


def total_height_big(instructions, total_n, shapes, offset, n_iter):
    tower, t, added_heights = set(), 0, []
    for i in range(n_iter):
        tower, t = add_shape(tower, shapes[i % len(shapes)], instructions, t)
        tower, h = clip_tower(tower)
        if i >= offset and h > 0:
            added_heights.append((i, h))
    period = find_period_in_list([h for _, h in added_heights])
    if period is None:
        print("Period not found")
        return
    iteration_period = added_heights[-1][0] - added_heights[-1 - period][0]

    def big_height(p, offset_periods=2):
        r = total_n % p
        ref = total_height(instructions, offset_periods * p + r, shapes)  # ref height
        incr = total_height(instructions, (offset_periods + 1) * p + r, shapes) - ref  # increment
        return ref + incr * (total_n // p - offset_periods)

    return big_height(iteration_period)


if __name__ == "__main__":
    aoc = AdventOfCodeDay(17, overwrite=False)
    data = aoc.load_strings()[0]

    print("Solution")
    print("  1.", total_height(data, 2022, shapes))
    print("  2.", total_height_big(data, 1000000000000, shapes, 200, 6000))
