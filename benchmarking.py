"""File to execute to produce benchmarks.

Parameters
---------------
    $1, n : int
        Maximum number of task
    $2, m : int
        Size of the batches for each number of task
    $3 $4, mini maxi : int int
        Max ranges for the tasks length


Author
---------
Adrien Pouyet

"""
import sys
import time
import pickle
import numpy as np

import nexter
import optimistic
import feasible
from data import *
from project import evaluate, branch_and_bound, johnson_naive


class Counter(object):
    """Just a counter."""

    def __init__(self):
        """Init total to 0."""
        self.total = 0

    def count(self):
        """Increment total."""
        self.total += 1


class Benchmarker(object):
    """Benchmarking class."""

    nexter_dict = {"n": nexter.naive, "a": nexter.fill_gaps_a_b, "b": nexter.fill_gaps_b_c}
    optimist_dict = {"n": optimistic.naive, "2": optimistic.b2, "4": optimistic.b4,
                     "1": optimistic.b1, "3": optimistic.b3}
    feas_dict = {"n": feasible.naive, "j": feasible.johnson}

    def __init__(self, case_generator, n, combos):
        """Init the benchamrker.

        Parameters
        -------------
            case_generator :
                Generator of case

        """
        self.case_generator = case_generator
        self.n = n
        self.fails = []
        self.times = {}

        for comb in combos:
            self.times[comb] = []

    def runall(self):
        """Run all cases."""
        for case in self.case_generator:
            tasks_a, tasks_d = case
            res = johnson_naive(tasks_a, self.n)
            remaining_tasks = list(tasks_d.keys())
            best_known = (res, evaluate(res, tasks_d, 3))
            for combo in self.times.keys():
                try:
                    nexter.FillGaps.init()
                    counter = Counter()

                    t = time.clock()
                    _, b = branch_and_bound([], remaining_tasks, best_known, tasks_d, 3, self.nexter_dict[combo[0]], self.optimist_dict[combo[1]], self.feas_dict[combo[2]], counter)
                    t = time.clock() - t

                    self.times[combo].append([t, b, counter.total, case])

                except Exception as e:
                    self.fails.append((case, combo, e))

    def save(self, filename):
        """Save self.times and self.fails."""
        with open(filename + "_times.complex", 'wb') as f:
            pickle.dump(self.times, f, pickle.HIGHEST_PROTOCOL)

        with open(filename + "_fails.complex", 'wb') as f:
            pickle.dump(self.fails, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    n = int(sys.argv[1])
    m = int(sys.argv[2])
#    mini = int(sys.argv[3])
#    maxi = int(sys.argv[4])
    all_combo = {}

    for ne in Benchmarker.nexter_dict.keys():
        for opt in Benchmarker.optimist_dict.keys():
            for fe in Benchmarker.feas_dict.keys():
                all_combo[(ne, opt, fe)] = 0

    print("Starting")
    for i in range(3, n):
        if all_combo == {}:
            break
        print("Cases of size", i, "is currently treated")
        cases = generate_cases_correle_onmachine(m, 3, i)

        bench = Benchmarker(cases, i, all_combo.keys())
        bench.runall()
<<<<<<< HEAD
        bench.save("time/benchmark_" + str(i) + "_tasks")
=======
        bench.save("3_time/benchmark_" + str(i) + "_tasks")
>>>>>>> 756e7e1dd8e4bfc85eeff589da386bdaed881870

        to_del = []
        for combo in all_combo:
            arr = np.asarray(bench.times[combo])
            if np.mean(arr[:, 0]) > 1:
                to_del.append(combo)
                print("Combo", combo, "has been removed")
        for c in to_del:
            del all_combo[c]

    print(time.clock())
