import networkx as nx
import matplotlib.pyplot as plt
import time
from pathlib import Path
import itertools as it
from subprocess import Popen
import math


def draw_graph_with_labels(
    G, red_vertices, blue_vertices, pos=None, with_labels=True, node_size=200, font_size=11
):
    cmap = []
    for vertex in G.nodes():
        if vertex in red_vertices:
            cmap.append("red")
        elif vertex in blue_vertices:
            cmap.append("blue")
        else:
            cmap.append("gray")
    nx.draw_networkx(
        G,
        pos=pos,
        node_color=cmap,
        with_labels=True,
        font_size=font_size,
        node_shape=".",
        node_size=node_size,
    )
    plt.show()


def textplot(red_vertices, m, n):
    output = ""
    for i in range(m):
        output = (
            output + " ".join(["o" if (i, j) in red_vertices else "." for j in range(n)]) + "\n"
        )
    print(output)


def grid_to_eps(red_vertices, m, n, name):
    factor = 0.3
    tikz_latex = f"""\\documentclass[a4paper,12pt]{{article}}
\\usepackage{{tikz}}
\\pgfrealjobname{{{name}_ext}}
\\begin{{document}}
\\beginpgfgraphicnamed{{{name}}}
\\begin{{tikzpicture}}"""
    for i, j in it.product(range(n), range(m)):
        if (j, i) in red_vertices:
            tikz_latex += f"\\fill[red] ({i}*{factor}, {m-j}*{factor}) circle (0.1cm);\n"
        else:
            tikz_latex += f"\\fill[blue] ({i}*{factor}, {m-j}*{factor}) circle (0.037cm);\n"

    tikz_latex += """\\end{tikzpicture}
\\endpgfgraphicnamed
\\end{document}"""
    with open(f"tmp/{name}.tex", "w", encoding="utf-8") as f:
        print(tikz_latex, file=f)
    Popen(["latex", "-output-directory", "tmp", f"tmp/{name}.tex"])
    time.sleep(10)
    Popen(["dvips", "-o", f"tmp/{name}.eps", f"tmp/{name}.dvi"])
    time.sleep(2)


def grids_to_eps(list_of_list_of_red_vertices, m, ns, name):
    factor = 0.3
    tikz_latex = f"""\\documentclass[a4paper,12pt]{{article}}
\\usepackage{{tikz}}
\\pgfrealjobname{{{name}_ext}}
\\begin{{document}}
\\beginpgfgraphicnamed{{{name}}}
\\begin{{tikzpicture}}"""
    for num, red_vertices in enumerate(list_of_list_of_red_vertices):
        n = ns[num]
        print(n, sum(ns[:num]))
        for i, j in it.product(range(n), range(m)):
            if (j, i) in red_vertices:
                tikz_latex += f"\\fill[red] ({(i+sum(ns[:num])+ 2*num)*factor}, {(m-j)*factor}) circle (0.1cm);\n"
            else:
                tikz_latex += f"\\fill[blue] ({(i+sum(ns[:num])+ 2*num)*factor}, {(m-j)*factor}) circle (0.037cm);\n"

    tikz_latex += """\\end{tikzpicture}
\\endpgfgraphicnamed
\\end{document}"""
    with open(f"tmp/{name}.tex", "w", encoding="utf-8") as f:
        print(tikz_latex, file=f)
    Popen(["latex", "-output-directory", "tmp", f"tmp/{name}.tex"])
    time.sleep(10)
    Popen(["dvips", "-o", f"tmp/{name}.eps", f"tmp/{name}.dvi"])
    time.sleep(2)


def triangle_to_eps(red_vertices, n, name):
    n = n + 1
    factor = 0.3
    tikz_latex = f"""\\documentclass[a4paper,12pt]{{article}}
\\usepackage{{tikz}}
\\pgfrealjobname{{{name}_ext}}
\\begin{{document}}
\\beginpgfgraphicnamed{{{name}}}
\\begin{{tikzpicture}}"""
    offset = 0
    node_id = 0
    for i in range(n):
        delta = 2 / math.sqrt(3)
        offset -= delta / 2
        for j in range(i + 1):
            if (i, j) in red_vertices:
                tikz_latex += (
                    f"\\fill[red] ({(j*delta+offset)*factor},  {(n-i)*factor}) circle (0.1cm);\n"
                )
            else:
                tikz_latex += (
                    f"\\fill[blue] ({(j*delta+offset)*factor}, {(n-i)*factor}) circle (0.037cm);\n"
                )
            node_id += 1
    tikz_latex += """\\end{tikzpicture}
\\endpgfgraphicnamed
\\end{document}"""
    with open(f"tmp/{name}_ext.tex", "w", encoding="utf-8") as f:
        print(tikz_latex, file=f)
    Popen(["latex", f"--jobname={name}", "-output-directory", "tmp", f"tmp/{name}_ext.tex"])
    time.sleep(10)
    Popen(["dvips", "-o", f"tmp/{name}.eps", f"tmp/{name}.dvi"])
    time.sleep(2)


if __name__ == "__main__":
    from knights_and_liars import kl_gurobi

    for n in range(4, 15 + 1):
        G = nx.grid_2d_graph(m=n, n=n, periodic=False)
        _, red_vertices, _ = kl_gurobi(G, OutputFlag=False, Threads=4)
        grid_to_eps(red_vertices, n, n, f"grid_{n}")

    Tor_12_27 = nx.grid_2d_graph(m=12, n=27, periodic=True)
    _, red_vertices, _ = kl_gurobi(Tor_12_27, OutputFlag=False, Threads=4)
    grid_to_eps(red_vertices, 12, 27, name="torus_12_27")

    Path_16 = nx.grid_2d_graph(m=1, n=16, periodic=False)
    _, red_vertices, _ = kl_gurobi(Path_16, OutputFlag=False, Threads=4)
    grid_to_eps(red_vertices, 1, 16, "grid_1_16")

    Grid_4_15 = nx.grid_2d_graph(m=4, n=15, periodic=False)
    _, red_vertices, _ = kl_gurobi(Grid_4_15, OutputFlag=False, Threads=4)
    grid_to_eps(red_vertices, 4, 16, "grid_4_15")

    Grid_7_32 = nx.grid_2d_graph(m=7, n=32, periodic=False)
    _, red_vertices, _ = kl_gurobi(Grid_7_32, OutputFlag=False, Threads=4)
    grid_to_eps(red_vertices, 7, 32, "grid_7_32")

    Grid_8_32 = nx.grid_2d_graph(m=8, n=32, periodic=False)
    _, red_vertices, _ = kl_gurobi(Grid_8_32, OutputFlag=False, Threads=4)
    grid_to_eps(red_vertices, 8, 32, "grid_8_32")

    tri_16_1 = [
        (0, 0),
        (1, 0),
        (2, 1),
        (2, 2),
        (3, 0),
        (3, 1),
        (3, 3),
        (4, 0),
        (4, 2),
        (4, 3),
        (5, 1),
        (5, 2),
        (5, 4),
        (5, 5),
        (6, 0),
        (6, 1),
        (6, 3),
        (6, 4),
        (6, 6),
        (7, 0),
        (7, 2),
        (7, 3),
        (7, 5),
        (7, 6),
        (8, 1),
        (8, 2),
        (8, 4),
        (8, 5),
        (8, 7),
        (8, 8),
        (9, 0),
        (9, 1),
        (9, 3),
        (9, 4),
        (9, 6),
        (9, 7),
        (9, 9),
        (10, 0),
        (10, 2),
        (10, 3),
        (10, 5),
        (10, 6),
        (10, 8),
        (10, 9),
        (11, 1),
        (11, 2),
        (11, 4),
        (11, 5),
        (11, 7),
        (11, 8),
        (11, 10),
        (11, 11),
        (12, 0),
        (12, 1),
        (12, 3),
        (12, 4),
        (12, 6),
        (12, 7),
        (12, 9),
        (12, 10),
        (12, 12),
        (13, 0),
        (13, 2),
        (13, 3),
        (13, 5),
        (13, 6),
        (13, 8),
        (13, 9),
        (13, 11),
        (13, 12),
        (14, 1),
        (14, 2),
        (14, 4),
        (14, 5),
        (14, 7),
        (14, 8),
        (14, 10),
        (14, 11),
        (14, 13),
        (14, 14),
        (15, 0),
        (15, 1),
        (15, 3),
        (15, 4),
        (15, 6),
        (15, 7),
        (15, 9),
        (15, 10),
        (15, 12),
        (15, 13),
        (15, 15),
        (16, 0),
        (16, 2),
        (16, 3),
        (16, 5),
        (16, 6),
        (16, 8),
        (16, 9),
        (16, 11),
        (16, 12),
        (16, 14),
        (16, 15),
    ]

    tri_16_2 = [
        (0, 0),
        (1, 0),
        (2, 1),
        (2, 2),
        (3, 0),
        (3, 1),
        (3, 3),
        (4, 0),
        (4, 2),
        (4, 3),
        (5, 1),
        (5, 2),
        (5, 4),
        (5, 5),
        (6, 0),
        (6, 1),
        (6, 3),
        (6, 4),
        (6, 6),
        (7, 0),
        (7, 2),
        (7, 3),
        (7, 5),
        (7, 6),
        (8, 1),
        (8, 2),
        (8, 4),
        (8, 5),
        (8, 7),
        (8, 8),
        (9, 0),
        (9, 1),
        (9, 3),
        (9, 4),
        (9, 6),
        (9, 7),
        (9, 9),
        (10, 0),
        (10, 2),
        (10, 3),
        (10, 5),
        (10, 6),
        (10, 8),
        (10, 9),
        (11, 1),
        (11, 2),
        (11, 4),
        (11, 5),
        (11, 7),
        (11, 8),
        (11, 10),
        (11, 11),
        (12, 0),
        (12, 1),
        (12, 3),
        (12, 4),
        (12, 6),
        (12, 7),
        (12, 9),
        (12, 10),
        (12, 12),
        (13, 0),
        (13, 2),
        (13, 3),
        (13, 5),
        (13, 6),
        (13, 8),
        (13, 9),
        (13, 11),
        (13, 13),
        (14, 1),
        (14, 2),
        (14, 4),
        (14, 5),
        (14, 7),
        (14, 8),
        (14, 10),
        (14, 11),
        (14, 12),
        (14, 13),
        (15, 0),
        (15, 1),
        (15, 3),
        (15, 4),
        (15, 6),
        (15, 7),
        (15, 9),
        (15, 10),
        (15, 14),
        (15, 15),
        (16, 0),
        (16, 2),
        (16, 3),
        (16, 5),
        (16, 6),
        (16, 8),
        (16, 9),
        (16, 11),
        (16, 12),
        (16, 13),
        (16, 14),
        (16, 16),
    ]

    opt_16 = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 11),
        (1, 12),
        (1, 13),
        (2, 1),
        (2, 4),
        (2, 7),
        (2, 9),
        (2, 10),
        (2, 11),
        (2, 13),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 7),
        (3, 8),
        (3, 12),
        (3, 13),
        (4, 8),
        (4, 9),
        (4, 11),
        (4, 12),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 9),
        (5, 10),
        (5, 11),
        (5, 13),
        (5, 14),
        (6, 5),
        (6, 7),
        (6, 8),
        (6, 13),
        (6, 14),
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 5),
        (7, 6),
        (7, 8),
        (7, 9),
        (8, 1),
        (8, 3),
        (8, 4),
        (8, 6),
        (8, 7),
        (8, 9),
        (9, 1),
        (9, 2),
        (9, 4),
        (9, 5),
        (9, 7),
        (9, 8),
        (9, 9),
        (9, 11),
        (9, 12),
        (9, 13),
        (10, 2),
        (10, 5),
        (10, 10),
        (10, 11),
        (10, 13),
        (11, 1),
        (11, 2),
        (11, 4),
        (11, 5),
        (11, 9),
        (11, 10),
        (11, 12),
        (11, 13),
        (12, 1),
        (12, 3),
        (12, 4),
        (12, 9),
        (12, 11),
        (12, 12),
        (13, 1),
        (13, 2),
        (13, 3),
        (13, 5),
        (13, 6),
        (13, 9),
        (13, 10),
        (13, 11),
        (13, 13),
        (13, 14),
        (14, 5),
        (14, 6),
        (14, 13),
        (14, 14),
    ]

    opt_17 = [
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 11),
        (1, 12),
        (1, 13),
        (2, 6),
        (2, 9),
        (2, 10),
        (2, 11),
        (2, 13),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 12),
        (3, 13),
        (4, 1),
        (4, 4),
        (4, 5),
        (4, 8),
        (4, 9),
        (4, 11),
        (4, 12),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 9),
        (5, 10),
        (5, 11),
        (5, 13),
        (5, 14),
        (5, 15),
        (6, 3),
        (6, 7),
        (6, 12),
        (6, 13),
        (6, 15),
        (7, 2),
        (7, 3),
        (7, 6),
        (7, 7),
        (7, 11),
        (7, 12),
        (7, 14),
        (7, 15),
        (8, 2),
        (8, 6),
        (8, 11),
        (8, 14),
        (9, 2),
        (9, 3),
        (9, 6),
        (9, 7),
        (9, 11),
        (9, 12),
        (9, 14),
        (9, 15),
        (10, 3),
        (10, 7),
        (10, 12),
        (10, 13),
        (10, 15),
        (11, 1),
        (11, 2),
        (11, 3),
        (11, 5),
        (11, 6),
        (11, 7),
        (11, 9),
        (11, 10),
        (11, 11),
        (11, 13),
        (11, 14),
        (11, 15),
        (12, 1),
        (12, 4),
        (12, 5),
        (12, 8),
        (12, 9),
        (12, 11),
        (12, 12),
        (13, 1),
        (13, 2),
        (13, 3),
        (13, 4),
        (13, 6),
        (13, 7),
        (13, 8),
        (13, 12),
        (13, 13),
        (14, 6),
        (14, 9),
        (14, 10),
        (14, 11),
        (14, 13),
        (15, 6),
        (15, 7),
        (15, 8),
        (15, 9),
        (15, 11),
        (15, 12),
        (15, 13),
    ]

    opt_18 = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 9),
        (1, 10),
        (1, 11),
        (2, 1),
        (2, 3),
        (2, 9),
        (2, 11),
        (2, 13),
        (2, 14),
        (2, 15),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 9),
        (3, 11),
        (3, 12),
        (3, 13),
        (3, 15),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 9),
        (4, 10),
        (4, 14),
        (4, 15),
        (5, 5),
        (5, 7),
        (5, 8),
        (5, 10),
        (5, 11),
        (5, 13),
        (5, 14),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 5),
        (6, 6),
        (6, 8),
        (6, 9),
        (6, 11),
        (6, 12),
        (6, 13),
        (6, 15),
        (6, 16),
        (7, 1),
        (7, 3),
        (7, 4),
        (7, 6),
        (7, 7),
        (7, 9),
        (7, 10),
        (7, 15),
        (7, 16),
        (8, 1),
        (8, 2),
        (8, 4),
        (8, 5),
        (8, 7),
        (8, 8),
        (8, 10),
        (8, 11),
        (9, 2),
        (9, 5),
        (9, 8),
        (9, 11),
        (10, 1),
        (10, 2),
        (10, 4),
        (10, 5),
        (10, 7),
        (10, 8),
        (10, 10),
        (10, 11),
        (11, 1),
        (11, 3),
        (11, 4),
        (11, 6),
        (11, 7),
        (11, 9),
        (11, 10),
        (11, 15),
        (11, 16),
        (12, 1),
        (12, 2),
        (12, 3),
        (12, 5),
        (12, 6),
        (12, 8),
        (12, 9),
        (12, 11),
        (12, 12),
        (12, 13),
        (12, 15),
        (12, 16),
        (13, 5),
        (13, 7),
        (13, 8),
        (13, 10),
        (13, 11),
        (13, 13),
        (13, 14),
        (14, 5),
        (14, 6),
        (14, 7),
        (14, 9),
        (14, 10),
        (14, 14),
        (14, 15),
        (15, 2),
        (15, 3),
        (15, 9),
        (15, 11),
        (15, 12),
        (15, 13),
        (15, 15),
        (16, 2),
        (16, 3),
        (16, 9),
        (16, 10),
        (16, 11),
        (16, 13),
        (16, 14),
        (16, 15),
    ]

    ex_20_160 = [
        (1, 1),
        (1, 2),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11),
        (1, 12),
        (1, 13),
        (1, 16),
        (1, 17),
        (1, 18),
        (2, 1),
        (2, 2),
        (2, 5),
        (2, 13),
        (2, 16),
        (2, 18),
        (3, 5),
        (3, 6),
        (3, 12),
        (3, 13),
        (3, 16),
        (3, 18),
        (4, 6),
        (4, 12),
        (4, 16),
        (4, 17),
        (4, 18),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 5),
        (5, 6),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 12),
        (5, 13),
        (5, 14),
        (6, 1),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 7),
        (6, 8),
        (6, 10),
        (6, 11),
        (6, 14),
        (7, 1),
        (7, 6),
        (7, 7),
        (7, 11),
        (7, 12),
        (7, 13),
        (7, 14),
        (7, 16),
        (7, 17),
        (7, 18),
        (8, 1),
        (8, 5),
        (8, 6),
        (8, 8),
        (8, 9),
        (8, 10),
        (8, 15),
        (8, 16),
        (8, 18),
        (9, 1),
        (9, 5),
        (9, 8),
        (9, 10),
        (9, 11),
        (9, 14),
        (9, 15),
        (9, 17),
        (9, 18),
        (10, 1),
        (10, 5),
        (10, 6),
        (10, 8),
        (10, 9),
        (10, 11),
        (10, 14),
        (10, 17),
        (11, 1),
        (11, 6),
        (11, 7),
        (11, 9),
        (11, 10),
        (11, 11),
        (11, 14),
        (11, 15),
        (11, 17),
        (11, 18),
        (12, 1),
        (12, 3),
        (12, 4),
        (12, 5),
        (12, 7),
        (12, 15),
        (12, 16),
        (12, 18),
        (13, 1),
        (13, 2),
        (13, 3),
        (13, 5),
        (13, 7),
        (13, 13),
        (13, 14),
        (13, 16),
        (13, 17),
        (13, 18),
        (14, 5),
        (14, 6),
        (14, 7),
        (14, 9),
        (14, 10),
        (14, 11),
        (14, 13),
        (14, 14),
        (15, 8),
        (15, 9),
        (15, 11),
        (15, 12),
        (16, 1),
        (16, 2),
        (16, 3),
        (16, 4),
        (16, 7),
        (16, 8),
        (16, 12),
        (16, 13),
        (16, 16),
        (16, 17),
        (16, 18),
        (17, 1),
        (17, 4),
        (17, 7),
        (17, 9),
        (17, 10),
        (17, 11),
        (17, 13),
        (17, 16),
        (17, 18),
        (18, 1),
        (18, 2),
        (18, 3),
        (18, 4),
        (18, 7),
        (18, 8),
        (18, 9),
        (18, 11),
        (18, 12),
        (18, 13),
        (18, 16),
        (18, 17),
        (18, 18),
    ]

    ex_19_144 = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 10),
        (1, 11),
        (1, 12),
        (1, 15),
        (1, 16),
        (1, 17),
        (2, 1),
        (2, 3),
        (2, 6),
        (2, 8),
        (2, 9),
        (2, 10),
        (2, 12),
        (2, 15),
        (2, 17),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 6),
        (3, 7),
        (3, 11),
        (3, 12),
        (3, 15),
        (3, 16),
        (3, 17),
        (4, 7),
        (4, 8),
        (4, 10),
        (4, 11),
        (5, 5),
        (5, 6),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 12),
        (5, 13),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 5),
        (6, 6),
        (6, 12),
        (6, 13),
        (6, 15),
        (6, 16),
        (6, 17),
        (7, 1),
        (7, 3),
        (7, 4),
        (7, 14),
        (7, 15),
        (7, 17),
        (8, 1),
        (8, 2),
        (8, 4),
        (8, 5),
        (8, 8),
        (8, 9),
        (8, 10),
        (8, 13),
        (8, 14),
        (8, 16),
        (8, 17),
        (9, 2),
        (9, 5),
        (9, 8),
        (9, 10),
        (9, 13),
        (9, 16),
        (10, 1),
        (10, 2),
        (10, 4),
        (10, 5),
        (10, 8),
        (10, 9),
        (10, 10),
        (10, 13),
        (10, 14),
        (10, 16),
        (10, 17),
        (11, 1),
        (11, 3),
        (11, 4),
        (11, 14),
        (11, 15),
        (11, 17),
        (12, 1),
        (12, 2),
        (12, 3),
        (12, 5),
        (12, 6),
        (12, 12),
        (12, 13),
        (12, 15),
        (12, 16),
        (12, 17),
        (13, 5),
        (13, 6),
        (13, 8),
        (13, 9),
        (13, 10),
        (13, 12),
        (13, 13),
        (14, 7),
        (14, 8),
        (14, 10),
        (14, 11),
        (15, 1),
        (15, 2),
        (15, 3),
        (15, 6),
        (15, 7),
        (15, 11),
        (15, 12),
        (15, 15),
        (15, 16),
        (15, 17),
        (16, 1),
        (16, 3),
        (16, 6),
        (16, 8),
        (16, 9),
        (16, 10),
        (16, 12),
        (16, 15),
        (16, 17),
        (17, 1),
        (17, 2),
        (17, 3),
        (17, 6),
        (17, 7),
        (17, 8),
        (17, 10),
        (17, 11),
        (17, 12),
        (17, 15),
        (17, 16),
        (17, 17),
    ]

    # Images for height 5
    pattern_5_1 = [(1, 1), (2, 2), (1, 2), (2, 1)]
    pattern_5_2 = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
    pattern_5_3 = [(1, 1), (1, 2), (1, 3), (1, 4), (3, 1), (3, 2), (3, 3), (3, 4), (2, 1), (2, 4)]
    grids_to_eps([pattern_5_1, pattern_5_2, pattern_5_3], 5, [4, 5, 6], "height_5_patterns")
    # Images for height 6
    pattern_6_1 = [(1, 1), (2, 2), (1, 2), (2, 1)]
    pattern_6_2 = [(1, 1), (2, 1), (3, 1), (4, 1), (1, 3), (2, 3), (3, 3), (4, 3), (1, 2), (4, 2)]
    grids_to_eps([pattern_6_1, pattern_6_2], 6, [4, 5], "height_6_patterns")

    grid_to_eps(opt_16, 16, 16, "grid_16")
    grid_to_eps(opt_17, 17, 17, "grid_17")
    grid_to_eps(opt_18, 18, 18, "grid_18")
    grid_to_eps(ex_19_144, 19, 19, "grid_19_lb")
    grid_to_eps(ex_20_160, 20, 20, "grid_20_lb")

    triangle_to_eps(tri_16_1, 16, "tri_16_1")
    triangle_to_eps(tri_16_2, 16, "tri_16_2")

