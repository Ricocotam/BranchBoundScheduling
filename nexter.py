"""Nexter functions.

Author
--------
Adrien Pouyet

"""


def naive(first_tasks, remaining_tasks, tasks_d):
    """Naive nexter. Yields next element in remaining_tasks."""
    for t in remaining_tasks:
        yield t


class FillGaps:
    """Class to store static data."""

    gaps_ab_arr = None
    gaps_bc_arr = None

    @staticmethod
    def init():
        """Set gaps_ab_arr and gaps_bc_arr to None."""
        FillGaps.gaps_ab_arr = None
        FillGaps.gaps_bc_arr = None

    @staticmethod
    def fill_gaps_a_b(first_tasks, remaining_tasks, tasks_d):
        """Try to fill gaps between machine A and machine B."""
        if FillGaps.gaps_ab_arr is None:
            FillGaps.gaps_ab_arr = sorted(first_tasks + remaining_tasks, key=lambda a: tasks_d[a][0] - tasks_d[a][1])

        i = 0
        left = 0
        right = -1
        last_was_b = True  # Last was long b short a
        while i < len(remaining_tasks):
            if last_was_b:
                while FillGaps.gaps_ab_arr[right] not in remaining_tasks:
                    right -= 1
                yield FillGaps.gaps_ab_arr[right]
                right -= 1
            else:
                while FillGaps.gaps_ab_arr[left] not in remaining_tasks:
                    left += 1
                yield FillGaps.gaps_ab_arr[left]
                left += 1
            last_was_b = ~last_was_b
            i += 1

    @staticmethod
    def fill_gaps_b_c(first_tasks, remaining_tasks, tasks_d):
        """Try to fill gaps between machine C and machine B."""
        if FillGaps.gaps_bc_arr is None:
            FillGaps.gaps_bc_arr = sorted(first_tasks + remaining_tasks, key=lambda a: tasks_d[a][1] - tasks_d[a][2])

        i = 0
        left = 0
        right = -1
        last_was_c = True  # Last was long c short b
        while i < len(remaining_tasks):
            if last_was_c:
                while FillGaps.gaps_bc_arr[right] not in remaining_tasks:
                    right -= 1
                yield FillGaps.gaps_bc_arr[right]
                right -= 1
            else:
                while FillGaps.gaps_ab_arr[left] not in remaining_tasks:
                    left += 1
                yield FillGaps.gaps_bc_arr[left]
                left += 1
            last_was_c = ~last_was_c
            i += 1


fill_gaps_a_b = FillGaps.fill_gaps_a_b
fill_gaps_b_c = FillGaps.fill_gaps_b_c
