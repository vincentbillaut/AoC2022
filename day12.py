import networkx as nx
import numpy as np
from itertools import product

from start_day import AdventOfCodeDay


def make_graph(input_grid):
    G = nx.DiGraph()
    grid = input_grid.copy()
    grid[grid == "S"] = "a"
    grid[grid == "E"] = "z"
    for i, j in product(range(grid.shape[0]), range(grid.shape[1])):
        G.add_node((i, j))
    for i, j in product(range(grid.shape[0]), range(grid.shape[1])):
        if i > 0 and ord(grid[i - 1, j]) - ord(grid[i, j]) <= 1:
            G.add_edge((i, j), (i - 1, j))
        if j > 0 and ord(grid[i, j - 1]) - ord(grid[i, j]) <= 1:
            G.add_edge((i, j), (i, j - 1))
        if i < grid.shape[0] - 1 and ord(grid[i + 1, j]) - ord(grid[i, j]) <= 1:
            G.add_edge((i, j), (i + 1, j))
        if j < grid.shape[1] - 1 and ord(grid[i, j + 1]) - ord(grid[i, j]) <= 1:
            G.add_edge((i, j), (i, j + 1))
    return G


def shortest_path(input_grid):
    G = make_graph(input_grid)
    start = np.where(input_grid == "S")[0][0], np.where(input_grid == "S")[1][0]
    end = np.where(input_grid == "E")[0][0], np.where(input_grid == "E")[1][0]
    return nx.shortest_path_length(G, source=start, target=end)


def find_best_starting_point(input_grid):
    G = make_graph(input_grid)
    start = np.where(input_grid == "S")[0][0], np.where(input_grid == "S")[1][0]
    end = np.where(input_grid == "E")[0][0], np.where(input_grid == "E")[1][0]
    other_starts = np.where(input_grid == "a")
    shortest_paths = [nx.shortest_path_length(G, source=start, target=end)]
    for i, j in zip(*other_starts):
        try:
            shortest_paths.append(nx.shortest_path_length(G, source=(i, j), target=end))
        except:
            pass
    return min(shortest_paths)


if __name__ == "__main__":
    aoc = AdventOfCodeDay(12, overwrite=True)
    grid = np.array([list(l) for l in aoc.load_strings()])

    print("Solution")
    print("  1.", shortest_path(grid))
    print("  2.", find_best_starting_point(grid))
