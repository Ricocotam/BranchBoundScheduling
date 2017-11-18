"""Execute the project. Give a case in stdin.

Author
--------
Adrien Pouyet

"""


from project import branch_and_bound, johnson_naive, evaluate
from data import * #read_case
import feasible
import optimistic
import nexter
import benchmarking
import time

def too_big(tasks_d):
    sum_dif = 0
    for task in tasks_d:
        sum_dif += abs(tasks_d[task][0] - tasks_d[task][1])
        sum_dif += abs(tasks_d[task][1] - tasks_d[task][2])
    return (sum_dif / len(tasks_d)) > 20

if __name__ == '__main__':
    tasks_a, tasks_d, nb = read_case()

    if too_big(tasks_d):
        n = nexter.fill_gaps_b_c
        o = optimistic.b1
        f = feasible.naive
        print("Combinaison choisie : 'b1n'")
    else:
        n = nexter.fill_gaps_a_b
        o = optimistic.b4
        f = feasible.naive
        print("Combinaison choisie : 'a4n'")

    res = johnson_naive(tasks_a, nb)

    remaining_tasks = list(tasks_d.keys())
    best_known = (res, evaluate(res, tasks_d, 3))
    counter = benchmarking.Counter()

    t = time.clock()
    a, b = branch_and_bound([], remaining_tasks, best_known, tasks_d, 3, n, o, f, counter)
    t = time.clock() - t
    print("Solution :", a, "; Valeur :",  b, "\nNombre de noeud explore :", counter.total, "; Temps CPU :", t)
