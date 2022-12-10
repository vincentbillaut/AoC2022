import numpy as np
from itertools import product
from start_day import AdventOfCodeDay


def ij_visible(i, j, mapp):
    # coordinate i, j is visible from one of the sides
    return (
        np.alltrue(mapp[i, j] > mapp[i, :j])
        or np.alltrue(mapp[i, j] > mapp[:i, j])
        or np.alltrue(mapp[i, j] > mapp[i, (j + 1) :])
        or np.alltrue(mapp[i, j] > mapp[(i + 1) :, j])
    )


def n_visible(mapp):
    is_visible = np.ones_like(mapp)
    n, m = mapp.shape
    for i, j in product(range(1, n - 1), range(1, m - 1)):
        is_visible[i, j] = int(ij_visible(i, j, mapp))
    return is_visible.sum()


def direction_view_ij(i, j, mapp, direction):
    n, m = mapp.shape
    height = mapp[i, j]
    vi, vj = direction
    xi, xj = i + vi, j + vj
    n_visible_in_direction = 0
    while 0 <= xi < n and 0 <= xj < m and mapp[xi, xj] < height:
        xi, xj = xi + vi, xj + vj
        n_visible_in_direction += 1
    if 0 <= xi < n and 0 <= xj < m:
        n_visible_in_direction += 1
    return n_visible_in_direction


def direction_view(mapp, direction):
    view = np.zeros_like(mapp)
    n, m = mapp.shape
    for i, j in product(range(n), range(m)):
        view[i, j] = direction_view_ij(i, j, mapp, direction)
    return view


def best_spot(mapp):
    return np.max(
        direction_view(mapp, (0, -1))
        * direction_view(mapp, (0, 1))
        * direction_view(mapp, (-1, 0))
        * direction_view(mapp, (1, 0))
    )


if __name__ == "__main__":
    aoc = AdventOfCodeDay(8, overwrite=True)
    data = np.array(aoc._load_all_lines(lambda l: list(map(int, l.strip()))))

    print("Solution")
    print("  1.", n_visible(data))
    print("  2.", best_spot(data))
