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
        red = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        high = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}
        low = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(red.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(red[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(high[x] + low[x] >= 1 - red[x])
                m.addConstr(high[x] + low[x] <= 1 + red[x])
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg / 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg / 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg / 2 + 1) * low[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg / 2 + 1) * high[x])

    elif formulation == "alternative":
        red = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        aux = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(red.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(red[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg / 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg / 2) * red[x])
                # if red[x] == 0 and aux[x] == 0, the strict minority of x's neighbors is red
                m.addConstr(
                    sum([red[y] for y in neighbors])
                    <= (deg / 2 - 1) + aux[x] * (deg / 2 + 1) + red[x] * (deg / 2 + 1)
                )
                # if red[x] == 0 and aux[x] == 1, the strict majority of x's neighbors is red
                m.addConstr(
                    sum([red[y] for y in neighbors])
                    >= (deg / 2 + 1) * aux[x] - (deg / 2 + 1) * red[x]
                )

    elif formulation == "indicator":
        red = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        high = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}
        low = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(red.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(red[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr((red[x] == 0) >> (high[x] + low[x] == 1))
                m.addConstr((red[x] == 1) >> (sum([red[y] for y in neighbors]) == (deg / 2)))
                m.addConstr((high[x] == 1) >> (sum([red[y] for y in neighbors]) <= deg / 2 - 1))
                m.addConstr((low[x] == 1) >> (sum([red[y] for y in neighbors]) >= deg / 2 + 1))

    if red_vertices is not None:
        for vertex in red_vertices:
            m.addConstr(red[vertex] == 1)

    if blue_vertices is not None:
        for vertex in blue_vertices:
            m.addConstr(red[vertex] == 0)

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

    if m.status == gp.GRB.OPTIMAL:
        return int(m.getAttr("ObjVal")), [v for v in red if red[v].X >= 0.95], "optimal"
    elif m.status == gp.GRB.TIME_LIMIT:
        try:
            return int(m.getAttr("ObjVal")), [v for v in red if red[v].X >= 0.95], "timelimit"
        except Exception as e:
            print("Timelimit hit, no feasible solution was found.")
            print(e)
            return None, None, "timelimit"
    elif m.status == gp.GRB.INFEASIBLE:
        return None, None, "infeasible"


def kl_mip(
    G,
    red_vertices=None,
    blue_vertices=None,
    formulation="standard",
    print_program=False,
    verbose=None,
    threads=None,
    emphasis=None,
):

    import mip

    m = mip.Model(sense=mip.MAXIMIZE, solver_name=mip.CBC)

    if print_program:
        with open(__file__) as f:
            print(f.read())

    if formulation == "standard":
        red = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes()}
        high = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}
        low = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.objective = mip.xsum(red.values())

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m += red[x] == 0
            else:
                neighbors = list(G.neighbors(x))
                m += high[x] + low[x] >= 1 - red[x]
                m += high[x] + low[x] <= 1 + red[x]
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg / 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg / 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg / 2 + 1) * low[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg / 2 + 1) * high[x]

    elif formulation == "alternative":
        red = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes()}
        aux = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.objective = mip.xsum(red.values())

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m += red[x] == 0
            else:
                neighbors = list(G.neighbors(x))
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg / 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg / 2) * red[x]
                # if red[x] == 0 and aux[x] == 0, the strict minority of x's neighbors is red
                m += mip.xsum([red[y] for y in neighbors]) <= (deg / 2 - 1) + aux[x] * (
                    deg / 2 + 1
                ) + red[x] * (deg / 2 + 1)
                # if red[x] == 0 and aux[x] == 1, the strict majority of x's neighbors is red
                m += (
                    mip.xsum([red[y] for y in neighbors])
                    >= (deg / 2 + 1) * aux[x] - (deg / 2 + 1) * red[x]
                )

    if red_vertices is not None:
        for vertex in red_vertices:
            m += red[vertex] == 1

    if blue_vertices is not None:
        for vertex in blue_vertices:
            m += red[vertex] == 0

    if verbose is not None:
        m.verbose = verbose

    if emphasis is not None:
        m.emphasis = emphasis

    if threads is not None:
        m.threads = threads

    m.max_gap = 0
    status = m.optimize()

    if status == mip.OptimizationStatus.OPTIMAL:
        return int(m.objective_value), [v for v in red if red[v].x >= 0.95], "optimal"

    elif status == mip.OptimizationStatus.INFEASIBLE:
        return None, None, "infeasible"


if __name__ == "__main__":
    # G = nx.hypercube_graph(12)
    # val, rv, status = kl_gurobi(
    #     G,
    #     red_vertices=[list(G.nodes())[0]],
    #     formulation="standard",
    #     OutputFlag=1,
    #     Threads=2,
    #     TimeLimit=0.0000001,
    # )
    # print(val, rv, status)

    G = nx.grid_graph(dim=[9, 9])

    val, rv, status = kl_mip(G, formulation="alternative", verbose=True, threads=1)
    print(val, rv, status)

    # start = time.time()
    # val, _, _ = kl_gurobi(G, formulation="alternative", OutputFlag=1, Threads=2)
    # print("alternative", val, time.time() - start)

    # start = time.time()
    # val, _, _ = kl_gurobi(G, formulation="standard", OutputFlag=1, Threads=2)
    # print("standard", val, time.time() - start)

    # start = time.time()
    # val, _, _ = kl_gurobi(G, formulation="indicator", OutputFlag=1, Threads=2)
    # print("indicator", val, time.time() - start)
