from utils.number_utils import is_integer_num
import numpy as np


def all_integers(solution):
    for _, value in solution.items():
        if not is_integer_num(value):
            return False
    return True


def first_non_integer(solution):
    for variable, value in solution.items():
        if not is_integer_num(value):
            return variable, value
    return None


def solution_is_better(first_solution, second_solution, min_max):
    if first_solution is None:
        return False
    if second_solution is None:
        return True

    if min_max == 'min':
        return first_solution['objective'] < second_solution['objective']
    else:
        return first_solution['objective'] > second_solution['objective']
