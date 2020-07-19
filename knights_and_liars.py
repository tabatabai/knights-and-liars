import networkx as nx
import time


def kl_gurobi(
    G,
    red_vertices=None,
    blue_vertices=None,
    formulation="standard",
    print_program=False,
    limit_hours=None,
    OutputFlag=None,
    Threads=None,
    MIPFocus=None,
    Symmetry=None,
    TimeLimit=None,
):

    import gurobipy as gp

    if print_program:
        with open(__file__) as f:
            print(f.read())

    m = gp.Model()

    if formulation not in ["standard", "alternative", "indicator"]:
        raise ValueError('The options for formulation are "standard", "alternative" or "indicator"')
    if formulation == "standard":
        label = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        high = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}
        low = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(label.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(label[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(high[x] + low[x] >= 1 - label[x])
                m.addConstr(high[x] + low[x] <= 1 + label[x])
                m.addConstr(sum([label[y] for y in neighbors]) <= deg - (deg / 2) * label[x])
                m.addConstr(sum([label[y] for y in neighbors]) >= (deg / 2) * label[x])
                m.addConstr(sum([label[y] for y in neighbors]) <= deg - (deg / 2 + 1) * low[x])
                m.addConstr(sum([label[y] for y in neighbors]) >= (deg / 2 + 1) * high[x])

    elif formulation == "alternative":
        label = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        aux = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(label.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(label[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(sum([label[y] for y in neighbors]) <= deg - (deg / 2) * label[x])
                m.addConstr(sum([label[y] for y in neighbors]) >= (deg / 2) * label[x])
                # following constraints must hold when label[x] == 0
                # if y == 0 the following constraint holds
                m.addConstr(
                    sum([label[y] for y in neighbors])
                    <= (deg / 2 - 1) + aux[x] * (deg / 2 + 1) + label[x] * (deg / 2 + 1)
                )
                # if y == 1 the following constraint holds
                m.addConstr(
                    sum([label[y] for y in neighbors])
                    >= (deg / 2 + 1) * aux[x] - (deg / 2 + 1) * label[x]
                )

    elif formulation == "indicator":
        label = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        high = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}
        low = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(label.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(label[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr((label[x] == 0) >> (high[x] + low[x] == 1))
                m.addConstr((label[x] == 1) >> (sum([label[y] for y in neighbors]) == (deg / 2)))
                m.addConstr((high[x] == 1) >> (sum([label[y] for y in neighbors]) <= deg / 2 - 1))
                m.addConstr((low[x] == 1) >> (sum([label[y] for y in neighbors]) >= deg / 2 + 1))

    if red_vertices is not None:
        for vertex in red_vertices:
            m.addConstr(label[vertex] == 1)

    if blue_vertices is not None:
        for vertex in blue_vertices:
            m.addConstr(label[vertex] == 0)

    if OutputFlag is not None:
        m.Params.OutputFlag = OutputFlag

    if Threads is not None:
        m.Params.Threads = Threads
    if MIPFocus is not None:
        m.Params.MIPFocus = MIPFocus
    if Symmetry is not None:
        m.Params.Symmetry = Symmetry
    if TimeLimit is not None:
        m.Params.TimeLimit = TimeLimit

    m.Params.MIPGap = 0

    m.optimize()
    try:
        return int(m.getAttr("ObjVal")), [x for x in label if label[x].X >= 0.95], m.status
    except:
        return None, None, None


if __name__ == "__main__":
    G = nx.grid_graph(dim=[12, 12])

    start = time.time()
    val, _, _ = kl_gurobi(G, formulation="alternative", OutputFlag=1, Threads=2)
    print("alternative", val, time.time() - start)

    start = time.time()
    val, _, _ = kl_gurobi(G, formulation="standard", OutputFlag=1, Threads=2)
    print("standard", val, time.time() - start)

    start = time.time()
    val, _, _ = kl_gurobi(G, formulation="indicator", OutputFlag=1, Threads=2)
    print("indicator", val, time.time() - start)
