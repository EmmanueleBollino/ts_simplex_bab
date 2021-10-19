import numpy as np

from lp_solver.branch_and_bound import BranchAndBound
from lp_solver.two_stage_simplex import TwoStageSimplex
from utils.file_utils import read_json
from utils.plot_utils import plot_2d_lp
from utils.print_utils import print_colored


def knapsack_problem():
    # OBJECTIVE: values of each item
    # CONSTRAINTS: first row weights of each item
    # CONSTRAINTS: other rows 1 for each item and 0 all the others
    # TERMS: first element maximum weight capacity
    # TERMS: other elements maximum multiplicity of each item
    # OPERATORS: all <=

    data = read_json('problems/knapsack.json')

    print_colored('KNAPSACK PROBLEM', 'teal')
    print('|{0:12}|{1:12}|{2:12}|{3:12}|'.format('Element', 'Value', 'Weight', 'Multiplicity'))
    for i in range(len(data['objective'])):
        print('|{0:12}|{1:12}|{2:12}|{3:12}|'.format(i, data['objective'][i], data['constraints'][0][i], data['terms'][i+1]))
    print('Maximum weight: {}'.format(data['terms'][0]))

    solver = BranchAndBound(constraints=data['constraints'],
                            terms=data['terms'],
                            operators=data['operators'],
                            objective=data['objective'],
                            min_max=data['min_max'],
                            lp_solver=TwoStageSimplex)

    solution = solver.solve()

    return solution
