def grid_bound(interval_sizes):
    term_1 = 2 / 3
    d = len(interval_sizes)
    for dim in interval_sizes:
        term_1 = term_1 * (dim - 2)
    prods = []
    for i in range(d):
        p = 1
        for j in range(d):
            if j != i:
                p *= interval_sizes[j] - 2
        prods.append(p)
    term_2 = 2 / (3 * d) * sum(prods)
    return term_1 + term_2


def tvb_step(G, tvb_vertices):
    if len(tvb_vertices) == 0:
        new_tvb_vertices = set([x for x in G.nodes() if G.degree[x] % 2 == 1])
    else:
        new_tvb_vertices = set()
        for x in G.nodes():
            neighbors = list(G.neighbors(x))
            if 2 * len([y for y in neighbors if y in tvb_vertices]) > G.degree[x]:
                new_tvb_vertices.add(x)
    return tvb_vertices.union(new_tvb_vertices)


def trivially_blue_vertices(G):
    tvb_vertices = set()
    while True:
        tvb_vertices_next = tvb_step(G, tvb_vertices)
        if tvb_vertices_next == tvb_vertices:
            return tvb_vertices
        else:
            tvb_vertices = tvb_vertices_next


if __name__ == "__main__":
    import networkx as nx

    print(grid_bound([800, 800, 800]), 2 / 3 * 800 ** 3)
    G = nx.grid_graph([10, 10])
    tvb = trivially_blue_vertices(G)
