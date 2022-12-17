import networkx as nx
import re
from itertools import product
from start_day import AdventOfCodeDay

pattern = re.compile(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

build_neighbor_dict = lambda inp: {v: l for v, _, l in inp}
build_rate_dict = lambda inp: {v: r for v, r, _ in inp}
valve_list_to_key = lambda l: "-".join(sorted(l))


def build_graph(inp):
    G, neighbors = nx.Graph(), build_neighbor_dict(inp)
    G.add_nodes_from(list(neighbors.keys()))
    for node in neighbors:
        G.add_edges_from([(node, n) for n in neighbors[node]])
    return G


def find_best_value(inp, start="AA", total_budget=30, elephant=False):
    G, rates = build_graph(inp), build_rate_dict(inp)
    non_zero_nodes = [v for v in rates if rates[v]]
    all_distances = nx.floyd_warshall(G)
    best_paths, memoize_valve_sets = {start: (0, total_budget)}, {}

    def update_paths(paths):
        new_paths, changed = {}, False
        for path, (score, budget) in paths.items():
            nodes_in_path = path.split("-")
            memoization_key = valve_list_to_key(nodes_in_path)
            memoize_valve_sets[memoization_key] = max(score, memoize_valve_sets.get(memoization_key, -1))
            if len(set(non_zero_nodes) - set(nodes_in_path)) == 0:
                new_paths[path] = score, budget
            for new_node in set(non_zero_nodes) - set(nodes_in_path):
                remaining_budget = budget - all_distances[nodes_in_path[-1]][new_node] - 1
                if remaining_budget >= 1:
                    new_paths[f"{path}-{new_node}"] = score + rates[new_node] * remaining_budget, remaining_budget
                    changed = True
                else:
                    new_paths[path] = score, budget
        return new_paths, changed and new_paths != paths

    changed = True
    while changed:
        best_paths, changed = update_paths(best_paths)

    best_pair_score = 0
    if elephant:
        for key1, key2 in product(memoize_valve_sets, memoize_valve_sets):
            set1, set2 = set(key1.split("-")[1:]), set(key2.split("-")[1:])
            if len(set1 & set2) == 0:
                best_pair_score = max(best_pair_score, memoize_valve_sets[key1] + memoize_valve_sets[key2])

    return best_pair_score if elephant else max(s for s, b in best_paths.values())


if __name__ == "__main__":
    aoc = AdventOfCodeDay(16, overwrite=True)
    data = [(v, int(r), list(l.split(", "))) for v, r, l in aoc.load_regex(pattern, 3)]

    print("Solution")
    print("  1.", find_best_value(data))
    print("  2.", find_best_value(data, total_budget=26, elephant=True))
