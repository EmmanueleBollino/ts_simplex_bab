import numpy as np

from problems.knapsack import knapsack_problem
from problems.toy import toy_problem
from utils.print_utils import print_colored


if __name__ == "__main__":
    solution = toy_problem()
    # solution = knapsack_problem()

    print_colored('\n---FINAL SOLUTION---', 'g')
    if solution is None:
        print_colored('No feasible solution found', 'r')
    elif solution is np.inf:
        print_colored('Solution diverges', 'y')
    else:
        print_colored(solution, 'dg')
