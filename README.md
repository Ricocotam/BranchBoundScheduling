# Branch and Bound

This is a project made for school. We had to find the best schedule so tasks finishes the fastest. Code is commented in english, images are the results of the benchmarks.
If you want the analysis of the benchmarks, ask me, I'm not going to put it in public but I can give on demand (for now only in french)

# The problem
You have 3 machines, $A, B and C$ and $n$ tasks. Each task has a specific need on each machine (might be different from a machine to another) and each task have to be executed in the order $A, B, C$ with no interruption (ie: if task 1 is the first on A and task 3 second on A, then it's the same order on B and C)
The project gave us some indications (Johnson algorithm and bounds $b_i, i \in \{1,2,3\}$) but we had to prove these were bounds. I also managed transforming the Johnson algorithm into linear and log linear algorithm. If you want to know how I might add it into the code.

