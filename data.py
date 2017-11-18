"""Everything related to data. Read and generate case.

Author
--------
Adrien Pouyet

"""

import numpy as np
import sys


def build_array(tasks_l, nb_task, nb_machine):
    """Build an array : list of (task duration, task id, machine id)."""
    tasks_a = []
    for i in range(nb_machine):
        for j in range(nb_task):
            tasks_a.append((tasks_l[i][j], j, i))
    return tasks_a


def build_dic(tasks_l, nb_tasks):
    """Build a dic : key is task id, value is task duration on each machine."""
    tasks_d = {}
    tasks = np.array(tasks_l)
    for i in range(nb_tasks):
        tasks_d[i] = tasks[:, i]
    return tasks_d


def read_case():
    """Read a case form sys.stdin."""
    n = int(sys.stdin.readline())
    tasks_l = []
    tasks_l.append(list(map(int, sys.stdin.readline().split(" "))))  # Read A
    tasks_l.append(list(map(int, sys.stdin.readline().split(" "))))  # Read B
    tasks_l.append(list(map(int, sys.stdin.readline().split(" "))))  # Read C
    return build_array(tasks_l, n, 3), build_dic(tasks_l, n), n


def random_case(nb_machine, nb_task, min_length, max_length):
    """Generate a random case."""
    tasks_l = np.random.randint(min_length, max_length+1, (nb_machine, nb_task))
    return build_array(tasks_l, nb_task, nb_machine), build_dic(tasks_l, nb_task)


def generate_cases(n, nb_machine, nb_task, min_length, max_length):
    """Generate n random_cases."""
    for i in range(n):
        yield random_case(nb_machine, nb_task, min_length, max_length)


def random_case_correle(nb_machine, nb_task):
    """Generate a random case."""
    tasks_l = []
    for i in range(nb_task):
        r_i = np.random.randint(0, 4+1)
        lo = 20*r_i
        hi = 20*r_i+20
        tasks_l.append(np.random.randint(lo, hi, 3))
    tasks_l = np.asarray(tasks_l).T
    return build_array(tasks_l, nb_task, nb_machine), build_dic(tasks_l, nb_task)


def generate_cases_correle(n, nb_machine, nb_task):
    """Generate n random_cases."""
    for i in range(n):
        yield random_case_correle(nb_machine, nb_task)


def random_case_correle_onmachine(nb_machine, nb_task):
    """Generate a random case."""
    tasks_l = []
    for i in range(nb_task):
        A = np.random.randint(1, 100)
        B = np.random.randint(16, 116)
        C = np.random.randint(31, 131)
        tasks_l.append([A, B, C])
    tasks_l = np.asarray(tasks_l).T
    return build_array(tasks_l, nb_task, nb_machine), build_dic(tasks_l, nb_task)


def generate_cases_correle_onmachine(n, nb_machine, nb_task):
    """Generate n random_cases."""
    for i in range(n):
        yield random_case_correle_onmachine(nb_machine, nb_task)
