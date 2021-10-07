# Knights and Liars on Graphs

Supplementary programs for the paper _Knights and Liars on Graphs_, by Paul Tabatabai and Dieter P. Gruber.

<p align="center">
  <img src="https://github.com/tabatabai/knights-and-liars/raw/master/ex.png" />
</p>

The paper is available in the Journal of Integer Sequences: <https://cs.uwaterloo.ca/journals/JIS/VOL24/Tabatabai/taba4.html>.

The paper deals with a combinatorial maximization problem, which is described in the sequence [A289362](https://oeis.org/A289362) of the Online Encyclopedia of Integer Sequences.
We studied the generalization of this problem to arbitrary (simple and undirected) graphs.

*Definition*:
The Knights and Liars number `kl(G)` of a graph `G` is the maximum possible number of red vertices in a red-blue-coloring of the vertices of `G`, such that for each red vertex, exactly half of its neighbors are red, and for each blue vertex, _not_ exactly half of its neighbors are red.

We give a short overview of the files' contents.
In `knights_and_liars.py`, we implement the functions `kl_gurobi`, using the offical Gurobi-API [`gurobipy`](https://www.gurobi.com/documentation/9.0/quickstart_linux/py_python_interface.html), and `kl_mip`, using the open source framework [`python-mip`](https://www.python-mip.com/).
By specifying the value of the parameter `formulation` it is possible to choose between different integer programming formulations for computing Knights and Liars numbers, as described in the paper.

The possible values of the parameter `formulation` for `kl_mip` are `"standard"`, `"bosch"`, `"alternative"`, `"bosch_subsets"` and  `"indicator"`. 
The possible values of the parameter `formulation` for `kl_mip` are `"standard"`, `"bosch"`, `"alternative"` and `"bosch_subsets"`.

In `utility.py`, the function `grid_bound` computes the bound from Proposition 2 of the paper and the function `trivially_blue_vertices` finds the trivially blue vertices of a given networkX-graph, as described in Section 2 of the paper.

In `plotting.py`, the functions `grid_to_eps`,  `grids_to_eps`, and  `triangle_to_eps` are for generating eps vector graphics, in the style used in the paper. The function `textplot` generates text representations of 2D grids, in the style of the OEIS-entry A289362. The function `draw_graph_with_labels` is used for plotting networkX-graphs with red and blue labels using matplotlib.
