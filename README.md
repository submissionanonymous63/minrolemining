# minrolemining

All rights reserved.

This repo is being made available for peer-review purposes only. Only authorized reviewers are allowed to access this
code, and run it, in any way.

Composition of this repo, most basic functionality first. All files have a main(), so one should be able to provide
a user-permission input file and run. We provide the running example that is used in the paper, Figure 1. One can also
get the examples from RMPLib: https://github.com/RMPlib/RMPlib/wiki . E.g., one can run: ./removedominatorsbp.py inputsup/rmplib/small/PLAIN_small_01.rmp

 - README.md: this readme file
 - readup.py: basic routines for reading the user-permission input, converting it to permission-users, etc.
 - removedominatorsbp.py: the algorithm from Section 3 of the paper; which is the Algorithm of Ene et al., while remaining in the world of bipartite graphs and bicliques
 - findcliquesbp.py: networkx's find_cliques() adapted to maximal bicliques in a bipartite graph
 - maxsetsbp.py: the algorithm from Section 4 that enumerate all maximal bicliques, reduces to ILP (1) and invokes gurobi to solve.
 - bicliquesbinsearch.py: the more natural reduction to LP + binary search
 - edgemaxbc.py: the code to search for large maximal bicliques. It invokes findcliquesbp above. Does require some manual intervention. Suggested use is to pipe stdout and stderr to a log file, and then read the log file.
 - mwis.py: the branch-and-price algorithm from Section 4.2; relies on a routine from constructg.py. Note that this works on the networkx version of the graph, i.e., after reduction to clique partition.
