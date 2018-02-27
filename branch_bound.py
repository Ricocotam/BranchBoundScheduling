"""Branch and bound class.

Author : Adrien Pouyet
"""


class Counter(object):
    """Just a counter."""

    def __init__(self):
        """Init total to 0."""
        self.total = 0

    def count(self):
        """Increment total."""
        self.total += 1


class BranchAndBound(object):
    """Class to have a simple to use branch&bound algorithm.

    Parameters
    -----------
        args : list, tuple, dir
            Container of the actions to take. It is the input of next functions

        evaluator : function
            Exact evaluation of a solution.

        nexter : function
            Get the next action

        optimistic : function
            Optimistic evaluation of a solution. Returns an upper bounded value

        feasible : function
            Get a feasible solution with its value.

        counter : Counter, optional
            Object to call if you want to know the number of node explored

        minimisation : bool, optional, default True
            True if you want you minimise else False

    Note
    ------
        1 - All listed functions must have the prototype:

            >>> def fun(first_actions, remaining_actions, args): pass

        2 - Values returned must implements __le__ or __ge__
    """

    def __init__(self, args, evaluator, nexter, optimistic, feasible, counter=None, minimisation=True):
        self.args = args
        self.nexter = nexter
        self.optimistic = optimistic
        self.feasible = feasible
        self.counter = counter
        self.minimisation = minimisation

    def run(self, first_actions, remaining_actions, best_known):
        """Run the branch and bound.

        Returns
        ---------
            solution : list
                Best feasible solution under the branch
            value : float
                Value of the solution, using evaluate function
        """
        if self.minimisation:
            if self.counter:
                return self._mini_count(first_actions, remaining_actions, best_known)
            else:
                return self._mini(first_actions, remaining_actions, best_known)
        else:
            if self.counter:
                return self._maxi_counter(first_actions, remaining_actions, best_known)
            else:
                return self._maxi(first_actions, remaining_actions, best_known)

    def _mini_counter(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value < best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            self.counter.count()
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            self.counter.count()
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v >= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] < best_known[1]:
                best_known = feas

            if feas[1] <= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._mini_counter(first_actions + [nt], rt, best_known)

        return best_known

    def _mini(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value < best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v >= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] < best_known[1]:
                best_known = feas

            if feas[1] <= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._mini(first_actions + [nt], rt, best_known)

        return best_known

    def _maxi_counter(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value > best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            self.counter.count()
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            self.counter.count()
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v <= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] > best_known[1]:
                best_known = feas

            if feas[1] >= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._maxi_counter(first_actions + [nt], rt, best_known)

        return best_known

    def _maxi(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value > best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v <= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] > best_known[1]:
                best_known = feas

            if feas[1] >= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._maxi(first_actions + [nt], rt, best_known)

        return best_known


class BranchAndBoundApprox(BranchAndBound):
    """Class to have a simple to use branch&bound algorithm.

    Parameters
    -----------
        min_diff : float
            Minimum improvement to explore the node. Always positive

        args : list, tuple, dir
            Container of the actions to take. It is the input of next functions

        evaluator : function
            Exact evaluation of a solution.

        nexter : function
            Get the next action

        optimistic : function
            Optimistic evaluation of a solution. Returns an upper bounded value

        feasible : function
            Get a feasible solution with its value.

        counter : Counter, optional
            Object to call if you want to know the number of node explored

        minimisation : bool, optional, default True
            True if you want you minimise else False

    Note
    ------
        1 - All listed functions must have the prototype:

            >>> def fun(first_actions, remaining_actions, args): pass
    """

    def __init__(self, min_diff, args, evaluator, nexter, optimistic, feasible, counter=None, minimisation=True):
        super(BranchAndBoundApprox, self).__init__(args, evaluator, nexter, optimistic, feasible, counter=None, minimisation=True)
        self.min_diff = min_diff if minimisation else -min_diff

    def _mini_counter(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value < best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            self.counter.count()
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            self.counter.count()
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v + self.min_diff >= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] < best_known[1]:
                best_known = feas

            if feas[1] <= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._mini_counter(first_actions + [nt], rt, best_known)

        return best_known

    def _mini(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value < best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v + self.min_diff >= best_known[1]:
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] < best_known[1]:
                best_known = feas

            if feas[1] <= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._mini(first_actions + [nt], rt, best_known)

        return best_known

    def _maxi_counter(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value > best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            self.counter.count()
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            self.counter.count()
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v + self.min_diff <= best_known[1]:  # self.min_diff is negative here
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] > best_known[1]:
                best_known = feas

            if feas[1] >= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._maxi_counter(first_actions + [nt], rt, best_known)

        return best_known

    def _maxi(self, first_actions, remaining_actions, best_known):
        if len(remaining_actions) <= 1:
            value = self.evaluate(first_actions + remaining_actions, self.args)
            if value > best_known[1]:
                best_known = (first_actions + remaining_actions, value)
            return best_known

        for nt in self.nexter(first_actions, remaining_actions, self.args):
            rt = [r for r in remaining_actions if r != nt]
            opt_v = self.optimistic(first_actions + [nt], rt, self.args)

            if opt_v + self.min_diff <= best_known[1]:  # self.min_diff is negative here
                return best_known

            feas = self.feasible(first_actions + [nt], rt, self.args)
            if feas[1] > best_known[1]:
                best_known = feas

            if feas[1] >= opt_v:
                return best_known

            # We're sure to get a lower or equal solution
            best_known = self._maxi(first_actions + [nt], rt, best_known)

        return best_known
