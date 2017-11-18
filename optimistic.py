"""Optimistic function.

Author
--------
Adrien Pouyet
"""

from project import evaluate_details


def naive(a, b, v):
    """Just return -1."""
    return -1


def b1(first_tasks, remaining_tasks, tasks_d):
    """b1."""
    t_a, t_b, t_c = evaluate_details(first_tasks, tasks_d, 3)

    rt_a = [tasks_d[rt][0] for rt in remaining_tasks]
    rt_b = [tasks_d[rt][1] for rt in remaining_tasks]

    t_b = max(t_a + min(rt_a), t_b)
    t_c = max(t_c, t_b + min(rt_b), t_a + min([a + b for a, b in zip(rt_a, rt_b)]))

    b_a = t_a + sum([tasks_d[rt][0] for rt in remaining_tasks]) + min(tasks_d[s][1] + tasks_d[s][2] for s in remaining_tasks)
    b_b = t_b + sum([tasks_d[rt][1] for rt in remaining_tasks]) + min(tasks_d[s][2] for s in remaining_tasks)
    b_c = t_c + sum([tasks_d[rt][2] for rt in remaining_tasks])

    return max(b_a, b_b, b_c)


def b2(first_tasks, remaining_tasks, tasks_d):
    """b2."""
    t_a, _, _ = evaluate_details(first_tasks, tasks_d, 3)
    k, value = max([(k, sum(tasks_d[k])) for k in remaining_tasks], key=lambda a: a[1])
    v = sum(tasks_d[rt][0] if tasks_d[rt][0] <= tasks_d[rt][2] else tasks_d[rt][2] for rt in remaining_tasks if rt != k)

    return t_a + value + v


def b3(first_tasks, remaining_tasks, tasks_d):
    """b3."""
    _, t_b, _ = evaluate_details(first_tasks, tasks_d, 3)
    k, value = max([(k, sum(tasks_d[k])) for k in remaining_tasks], key=lambda a: a[1])
    v = sum(tasks_d[rt][1] if tasks_d[rt][1] <= tasks_d[rt][2] else tasks_d[rt][2] for rt in remaining_tasks if rt != k)

    return t_b + value + v


def b4(first_tasks, remaining_tasks, tasks_d):
    """b3 but using t'_B^pi instead of just t_B^pi."""
    t_a, t_b, _ = evaluate_details(first_tasks, tasks_d, 3)
    t_b = max(t_b, t_a + min([tasks_d[rt][0] for rt in remaining_tasks]))
    k, value = max([(k, sum(tasks_d[k])) for k in remaining_tasks], key=lambda a: a[1])
    v = sum(tasks_d[rt][1] if tasks_d[rt][1] <= tasks_d[rt][2] else tasks_d[rt][2] for rt in remaining_tasks if rt != k)

    return t_b + value + v
