"""Feasible solution functions.

Author
-------
Adrien Pouyet

"""

from project import johnson_naive, evaluate


def naive(first_tasks, remaining_tasks, tasks_d):
    """Compute the feasible solution as first_tasks + remaining_tasks."""
    return first_tasks + remaining_tasks, evaluate(first_tasks + remaining_tasks, tasks_d, 3)


def johnson(first_tasks, remaining_tasks, tasks_d):
    """Use Johnson algorithm to find a solution."""
    r_tasks_a = []

    for i, rt in enumerate(remaining_tasks):
        r_tasks_a.extend([(t, rt, j) for j, t in enumerate(tasks_d[rt])])

    solution = first_tasks + johnson_naive(r_tasks_a, len(remaining_tasks))
    return solution, evaluate(solution, tasks_d, 3)
