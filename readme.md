# Knights and Liars on graphs

In this repository, we provide supplementary programs for the paper
_Knights and Liars on graphs_, which is co-authored by Dieter P. Gruber.
The paper has been submitted to the Journal of Integer sequences and is currently pending review. The submitted version will soon be available on arXiv.org.

The paper deals with a combinatorial maximization problem, which is described in the sequence [A289362](https://oeis.org/A289362) of the Online Encyclopedia of Integer Sequences.

We give a short overview of the files' contents.
* `knights_and_liars.py` 
    - This program contains various ways to model the Knights and Liars problem as an integer program.
    - The function `kl_gurobi` contains the IP formulation as given in the paper.
    - The function `kl_gurobi_indicator` uses indicator constraints to directly model the implications (5)-(7) from the paper.
    - The function `kl_gurobi_alt` contains an alternative way to model the problem. We have found this way to perform worse, but it might depend on the input graph.
    - The functions `kl_mip` and `kl_mip_alt` implement the same IPs as `kl_gurobi`  and `kl_gurobi_alt`, but uses the framework `python-mip`. This allows the use of the open source solver CBC. 
* ` utility.py` 
    - The function `grid_bound` computes the bound from Proposition 2 of the paper.
    - The function `trivially_blue_vertices` finds the trivially blue vertices of a given networkX-graph.
* ` plotting.py` 
    - The function `todo` generates nice-looking eps vector graphics of 2D grid configurations,
    in the style used in the paper.
    - The function `textplot` generaties text representations of the grids, in the style of the OEIS-entry A289362.
    - The function `draw_with_labels` is for plotting networkX-graphs with red and blue labels using matplotlib.
