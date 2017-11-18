"""Project of the COMPLEX class.

Author
--------
Adrien Pouyet

"""

from collections import deque


def evaluate(schedule, tasks_d, nb_machine):
    """Compute the end of scheduling.

    Parameters
    ----------
    schedule : list
        The tasks_d in the order you want

    tasks_d : {task:(d_a, d_b, ...)}

    """
    a = [tasks_d[s][0] for s in schedule]
    machines = []
    machines.append([a[0]])

    for i in range(1, len(a)):
        machines[0].append(a[i] + machines[0][i-1])

    for m_i in range(1, nb_machine):
        machines.append([machines[m_i - 1][0] + tasks_d[schedule[0]][m_i]])

        for i, s in enumerate(schedule[1:], start=1):
            machines[m_i].append(max(machines[m_i-1][i], machines[m_i][i-1]) + tasks_d[s][m_i])

    return machines[-1][-1]


def evaluate_details(schedule, tasks_d, nb_machine):
    """Compute the end of scheduling but returns all ends."""
    a = [tasks_d[s][0] for s in schedule]
    machines = []
    machines.append([a[0]])

    for i in range(1, len(a)):
        machines[0].append(a[i] + a[i-1])

    for m_i in range(1, nb_machine):
        machines.append([machines[m_i - 1][0] + tasks_d[schedule[0]][m_i]])

        for i, s in enumerate(schedule[1:], start=1):
            machines[m_i].append(max(machines[m_i-1][i], machines[m_i][i-1]) + tasks_d[s][m_i])

    return [machines[i][-1] for i in range(nb_machine)]


def branch_and_bound(first_tasks, remaining_tasks, best_known, tasks_d, nb_machine, next_tasker, optimistic, feasible, counter):
    """Branch and bound algorithm.

    Note
    ------
    This is a branch and bound algorithm for a maximisation. If you want
    minimisation, just minus all values

    Parameters
    -------------
    first_tasks : list
        First tasks picked

    remaining_tasks : list
        Remaining tasks we have to pick

    best_known : tuple(tasks, value)
        Best solution known so far. best_known[0] is the list of tasks,
        best_known[1] is its value

    tasks_d : dict
        Task dictionnary, returned by readfile.build_dic

    nb_machine : int
        Number of machines

    next_tasker : generator(first_tasks, remaining_tasks, tasks_d)
        Function which determine next task to pick. We use it to try different
        strategies

    optimistic : function(first_tasks, reamining_tasks, tasks_d), optionnal
        Function which determine an upper bound of the branch. We use it to try
        different strategies. Returns upper bound value.

    feasible : function(first_tasks, reamining_tasks, tasks_d)
        Function which determine a lower bound (also called feasible solution value)
        of the branch. We use it to try different strategies. Returns lower bound value and solution

    counter : function()
        Function that counts the number it's called. Used to know the number of nodes explorated.
        It is static and not recursive dependent


    Return
    ---------
    solution : list
        Best feasible solution under the branch
    value : float
        Value of the solution, using evaluate function

    """
    if len(remaining_tasks) <= 1:
        value = evaluate(first_tasks + remaining_tasks, tasks_d, nb_machine)
        if value < best_known[1]:
            best_known = (first_tasks + remaining_tasks, value)
        counter.count()
        return best_known

    for nt in next_tasker(first_tasks, remaining_tasks, tasks_d):
        counter.count()
        rt = [r for r in remaining_tasks if r != nt]

        opt_v = optimistic(first_tasks + [nt], rt, tasks_d)
        if opt_v >= best_known[1]:
            continue

        feas = feasible(first_tasks + [nt], rt, tasks_d)
        if feas[1] < best_known[1]:
            best_known = feas

        if feas[1] <= opt_v:
            return best_known

        # We're sure to get a lower or equal solution
        best_known = branch_and_bound(first_tasks + [nt], rt, best_known, tasks_d, nb_machine, next_tasker, optimistic, feasible, counter)

    return best_known


def branch_and_bound_approx(first_tasks, remaining_tasks, best_known, tasks_d, nb_machine, next_tasker, optimistic, feasible, counter, min_diff):
    """Branch and bound algorithm.

    Note
    ------
    This is a branch and bound algorithm for a maximisation. If you want
    minimisation, just minus all values

    Parameters
    -------------
    first_tasks : list
        First tasks picked

    remaining_tasks : list
        Remaining tasks we have to pick

    best_known : tuple(tasks, value)
        Best solution known so far. best_known[0] is the list of tasks,
        best_known[1] is its value

    tasks_d : dict
        Task dictionnary, returned by readfile.build_dic

    nb_machine : int
        Number of machines

    next_tasker : generator(first_tasks, remaining_tasks, tasks_d)
        Function which determine next task to pick. We use it to try different
        strategies

    optimistic : function(first_tasks, reamining_tasks, tasks_d), optionnal
        Function which determine an upper bound of the branch. We use it to try
        different strategies. Returns upper bound value.

    feasible : function(first_tasks, reamining_tasks, tasks_d)
        Function which determine a lower bound (also called feasible solution value)
        of the branch. We use it to try different strategies. Returns lower bound value and solution

    counter : function()
        Function that counts the number it's called. Used to know the number of nodes explorated.
        It is static and not recursive dependent

    min_diff : int
        Minimum value you can earn. Must be positive. If 0 it's like classic branch_and_bound


    Return
    ---------
    solution : list
        Best feasible solution under the branch
    value : float
        Value of the solution, using evaluate function

    """
    if len(remaining_tasks) <= 1:
        value = evaluate(first_tasks + remaining_tasks, tasks_d, nb_machine)
        if value < best_known[1]:
            best_known = (first_tasks + remaining_tasks, value)
        counter.count()
        return best_known

    for nt in next_tasker(first_tasks, remaining_tasks, tasks_d):
        counter.count()
        rt = [r for r in remaining_tasks if r != nt]
        opt_v = optimistic(first_tasks + [nt], rt, tasks_d)

        if opt_v + min_diff >= best_known[1]:
            return best_known

        feas = feasible(first_tasks + [nt], rt, tasks_d)
        if feas[1] < best_known[1]:
            best_known = feas

        if feas[1] <= opt_v:
            return best_known

        # We're sure to get a lower or equal solution
        best_known = branch_and_bound(first_tasks + [nt], rt, best_known, tasks_d, nb_machine, next_tasker, optimistic, feasible, counter)

    return best_known


def explore_leaves(tasks_a, tasks_d, nb_task, nb_machine):
    """Explore all leaves."""
    def permute(tasks):
        if len(tasks) <= 1:
            return [tasks[0]]

        ret = []
        permutations = permute(tasks[1:])

        for perm in permutations:
            ret.append(tasks[0] + perm)
            ret.append(perm + tasks[0])

        return ret

    tasks = list(range(nb_task))
    permutations = permute(tasks)

    values = []
    for perm in permutations:
        values.append((perm, evaluate(perm)))
    return values


def johnson_naive(tasks_a, nb_task):
    """Naive implementation of Johnson algorithm."""
    left = deque()
    right = deque()

    for i in range(nb_task):
        # (d, i, j)
        mini = tasks_a[0]
        for t in tasks_a[1:]:
            if t[0] < mini[0]:
                mini = t

        if mini[2] == 0:
            left.append(mini[1])
        else:
            right.appendleft(mini[1])

        j = 0
        while j < len(tasks_a):
            if tasks_a[j][1] == mini[1]:
                del tasks_a[j]
            else:
                j += 1

    if len(left) > 0 and len(right) > 0:
        left.extend(list(right))
        return list(left)
    elif len(left) > 0:
        return list(left)
    else:
        return list(right)
