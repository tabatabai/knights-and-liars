import networkx as nx
import matplotlib.pyplot as plt
import time
from pathlib import Path
import itertools as it
from subprocess import Popen


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


def grid_to_eps(red_vertices, m, n, name):
    factor = 0.3
    tikz_latex = """\\documentclass[a4paper,12pt]{article}
    \\usepackage{tikz}
    \\usepackage[psfixbb,graphics,tightpage,active]{preview}
    \\PreviewEnvironment{tikzpicture}
    \\begin{document}
    \\begin{tikzpicture}"""

    for i, j in it.product(range(n), range(m)):
        if (j, i) in red_vertices:
            tikz_latex += f"\\fill[red] ({i}*{factor}, {m-j}*{factor}) circle (0.1cm);\n"
        else:
            tikz_latex += f"\\fill[blue] ({i}*{factor}, {m-j}*{factor}) circle (0.037cm);\n"

    tikz_latex += """\\end{tikzpicture}
    \\end{document}"""
    Path("tmp").mkdir(exist_ok=True)
    with open(f"tmp/{name}.tex", "w", encoding="utf-8") as f:
        print(tikz_latex, file=f)
    Popen(["latex", "-output-directory", "tmp", f"tmp/{name}.tex"])
    time.sleep(10)
    Popen(["dvips", "-E", "-o", f"tmp/{name}.eps", f"tmp/{name}.dvi"])
    time.sleep(5)


def textplot(lorp, m, n):
    output = ""
    for i in range(m):
        output = output + " ".join(["o" if (i, j) in lorp else "." for j in range(n)]) + "\n"
    print(output)


if __name__ == "__main__":
    G = nx.grid_graph([4, 4])
    red_vertices = [(1, 1), (2, 2), (1, 2), (2, 1)]
    blue_vertices = [v for v in G.nodes() if v not in red_vertices]
    # draw_graph_with_labels(G, red_vertices, blue_vertices)

    textplot(red_vertices, 4, 4)

    # grid_to_eps(red_vertices, m=4, n=4, name="4x4_grid")

