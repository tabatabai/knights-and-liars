# Knights and Liars on Graphs

In this repository, we provide supplementary programs for the paper
_Knights and Liars on graphs_, which is co-authored by Dieter P. Gruber.
The paper has been submitted to the Journal of Integer sequences and is currently pending review. The submitted version will soon be available on arXiv.org.

The paper deals with a combinatorial maximization problem, which is described in the sequence [A289362](https://oeis.org/A289362) of the Online Encyclopedia of Integer Sequences.

We give a short overview of the files' contents.
In `knights_and_liars.py`, we implement the functions `kl_gurobi`, using the offical Gurobi-API gurobipy, and `kl_mip`, using
the open source framefork python-mip.
By specifying the parameter `formulation` for `kl_gurobi`, it is possible to choose between different integer programming formulations for computing Knights and Liars numbers.
The possible values of the parameter `formulation` for `kl_gurobi` are:
 - "standard", which is the formulation given in the paper.
 - "alternative", which is an alternative formulation, using fewer variables and constraints. We found this formulation to perform worse for two-dimensional grid graphs, but found performance gains for some other graphs.
 - "indicator", which is an implementation of "standard", but uses Gurobi's ability to directly model indicator constraints to directly model the implications (5)-(7) from the paper.
 The possible values of the parameter `formulation` for `kl_mip` are "standard" and "alternative".

In `utility.py`, the function `grid_bound` computes the bound from Proposition 2 of the paper and the function `trivially_blue_vertices` finds the trivially blue vertices of a given networkX-graph.

In `plotting.py`, he function `tikzplot` generates eps vector graphics of 2D grid configurations, in the style used in the paper. The function `textplot` generaties text representations of the grids, in the style of the OEIS-entry A289362. The function `draw_with_labels` is for plotting networkX-graphs with red and blue labels using matplotlib.
