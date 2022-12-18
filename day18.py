import networkx as nx
from start_day import AdventOfCodeDay

neighbors = lambda cube: {
    (cube[0] + 1, cube[1], cube[2]),
    (cube[0] - 1, cube[1], cube[2]),
    (cube[0], cube[1] + 1, cube[2]),
    (cube[0], cube[1] - 1, cube[2]),
    (cube[0], cube[1], cube[2] + 1),
    (cube[0], cube[1], cube[2] - 1),
}

count_exposed_sides = lambda cubes: sum((6 - len(cubes & neighbors(cube))) for cube in cubes)


def blow_up_set(s, bounds):
    final_s, n = final_s.union(*[neighbors(n) for n in final_s]) - bounds, len(s)
    while len(final_s) > n:
        n = len(final_s)
        final_s = final_s.union(*[neighbors(n) for n in final_s]) - bounds
    return final_s


def air_pockets(cubes):
    neighboring_cubes = set.union(*[neighbors(n) for n in cubes]) - cubes
    exterior_cubes = set.union(neighboring_cubes, *[neighbors(n) for n in neighboring_cubes]) - cubes
    exterior_ref_high = list(sorted(exterior_cubes, key=lambda x: x[2]))[-1]
    G = nx.Graph()
    G.add_nodes_from(exterior_cubes)
    for node in exterior_cubes:
        G.add_edges_from([(node, n) for n in neighbors(node) if n in exterior_cubes])
    return set.union(*[blow_up_set(cc, cubes) for cc in nx.connected_components(G) if exterior_ref_high not in cc])


final_surface = lambda inp: count_exposed_sides(inp) - count_exposed_sides(air_pockets(inp))

if __name__ == "__main__":
    aoc = AdventOfCodeDay(18, overwrite=False)
    data = set([(int(l.split(",")[0]), int(l.split(",")[1]), int(l.split(",")[2])) for l in aoc.load_strings()])

    print("Solution")
    print("  1.", count_exposed_sides(data))
    print("  2.", final_surface(data))
