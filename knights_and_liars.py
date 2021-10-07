import networkx as nx
import time
import itertools as it


def kl_gurobi(
    G,
    red_vertices=None,
    blue_vertices=None,
    formulation="standard",
    print_program=False,
    drop_optional=False,
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

    if formulation not in [
        "standard",
        "bosch",
        "bosch_subsets",
        "alternative",
        "indicator",
    ]:
        raise ValueError(
            'The options for formulation are "standard",'
            '"bosch_subsets", "alternative", or "indicator"'
        )
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
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg // 2) * red[x])
                if not drop_optional:
                    m.addConstr(high[x] + low[x] <= 1 + red[x])
                m.addConstr(high[x] + low[x] >= 1 - red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg // 2 + 1) * high[x])
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg // 2 + 1) * low[x])

    if formulation == "bosch":
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
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg // 2) * red[x])
                if not drop_optional:
                    m.addConstr(high[x] + low[x] >= 1 + red[x])
                m.addConstr(high[x] + low[x] <= 1 + red[x])

                m.addConstr(
                    sum([red[y] for y in neighbors]) >= (deg // 2 + 1) - (deg // 2 + 1) * high[x]
                )
                m.addConstr(
                    sum([red[y] for y in neighbors]) <= (deg // 2 - 1) + (deg // 2 + 1) * low[x]
                )

    if formulation == "bosch_subsets":
        red = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}

        m.setObjective(sum(red.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(red[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg // 2) * red[x])
                for S in it.combinations(neighbors, deg // 2):
                    T = [neighbor for neighbor in neighbors if neighbor not in S]
                    m.addConstr(
                        -red[x] + sum([red[s] for s in S]) - sum([red[t] for t in T])
                        <= deg // 2 - 1
                    )

    if formulation == "alternative":
        red = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes()}
        aux = {x: m.addVar(vtype=gp.GRB.BINARY) for x in G.nodes() if G.degree(x) % 2 == 0}

        m.setObjective(sum(red.values()), gp.GRB.MAXIMIZE)

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m.addConstr(red[x] == 0)
            else:
                neighbors = list(G.neighbors(x))
                m.addConstr(sum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x])
                m.addConstr(sum([red[y] for y in neighbors]) >= (deg // 2) * red[x])
                m.addConstr(
                    sum([red[y] for y in neighbors])
                    <= (deg // 2 - 1) + aux[x] * (deg // 2 + 1) + red[x] * (deg // 2 + 1)
                )
                m.addConstr(
                    sum([red[y] for y in neighbors])
                    >= (deg // 2 + 1) * aux[x] - (deg // 2 + 1) * red[x]
                )

    if formulation == "indicator":
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
                m.addConstr((red[x] == 1) >> (sum([red[y] for y in neighbors]) == (deg // 2)))
                m.addConstr((high[x] == 1) >> (sum([red[y] for y in neighbors]) <= deg // 2 - 1))
                m.addConstr((low[x] == 1) >> (sum([red[y] for y in neighbors]) >= deg // 2 + 1))

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
        return round(m.getAttr("ObjVal")), [v for v in red if red[v].X >= 0.95], "optimal"
    elif m.status == gp.GRB.TIME_LIMIT:
        try:
            return round(m.getAttr("ObjVal")), [v for v in red if red[v].X >= 0.95], "timelimit"
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

    if print_program:
        with open(__file__) as f:
            print(f.read())

    m = mip.Model(sense=mip.MAXIMIZE, solver_name=mip.CBC)

    if formulation not in [
        "standard",
        "bosch",
        "bosch_subsets",
        "alternative",
    ]:
        raise ValueError(
            'The options for formulation are "standard",' '"bosch_subsets", or "alternative"'
        )

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
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg // 2) * red[x]
                m += high[x] + low[x] <= 1 + red[x]
                m += high[x] + low[x] >= 1 - red[x]
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg // 2 + 1) * low[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg // 2 + 1) * high[x]

    elif formulation == "bosch":
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
                m += sum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x]
                m += sum([red[y] for y in neighbors]) >= (deg // 2) * red[x]
                m += high[x] + low[x] >= 1 + red[x]
                m += high[x] + low[x] <= 1 + red[x]
                m += sum([red[y] for y in neighbors]) >= (deg // 2 + 1) - (deg // 2 + 1) * high[x]
                m += sum([red[y] for y in neighbors]) <= (deg // 2 - 1) + (deg // 2 + 1) * low[x]

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
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg // 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) <= (deg // 2 - 1) + aux[x] * (
                    deg // 2 + 1
                ) + red[x] * (deg // 2 + 1)
                m += (
                    mip.xsum([red[y] for y in neighbors])
                    >= (deg // 2 + 1) * aux[x] - (deg // 2 + 1) * red[x]
                )

    if formulation == "bosch_subsets":
        red = {x: m.add_var(var_type=mip.BINARY) for x in G.nodes()}

        m.objective = mip.xsum(red.values())

        for x in G.nodes():
            deg = G.degree[x]
            if deg % 2 == 1:
                m += red[x] == 0
            else:
                neighbors = list(G.neighbors(x))
                m += mip.xsum([red[y] for y in neighbors]) <= deg - (deg // 2) * red[x]
                m += mip.xsum([red[y] for y in neighbors]) >= (deg // 2) * red[x]
                for S in it.combinations(neighbors, deg // 2):
                    T = [neighbor for neighbor in neighbors if neighbor not in S]
                    m += (
                        -red[x] + sum([red[s] for s in S]) - sum([red[t] for t in T])
                        <= deg // 2 - 1
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
        return round(m.objective_value), [v for v in red if red[v].x >= 0.95], "optimal"

    elif status == mip.OptimizationStatus.INFEASIBLE:
        return None, None, "infeasible"


if __name__ == "__main__":
    G = nx.grid_graph(dim=[7, 7])
    for formulation in ["alternative", "standard", "bosch", "bosch_subsets"]:
        val, rv, status = kl_mip(G, formulation="alternative", verbose=False, threads=1)
        print(val, rv, status)
        val, rv, status = kl_gurobi(G, formulation="alternative", OutputFlag=False, Threads=1)
        print(val, rv, status)
