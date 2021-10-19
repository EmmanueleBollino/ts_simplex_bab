import numpy as np

from lp_solver.branch_and_bound import BranchAndBound
from lp_solver.two_stage_simplex import TwoStageSimplex
from utils.file_utils import read_json
from utils.plot_utils import plot_2d_lp
from utils.print_utils import print_colored


def toy_problem():
    data = read_json('problems/toy.json')

    solver = BranchAndBound(constraints=data['constraints'],
                            terms=data['terms'],
                            operators=data['operators'],
                            objective=data['objective'],
                            min_max=data['min_max'],
                            lp_solver=TwoStageSimplex)

    solution = solver.solve()

    # plot
    if len(data['constraints'][0]) == 2 and solution is not None and solution != np.inf:
        plot_2d_lp(constraints=data['constraints'],
                   terms=data['terms'],
                   operators=data['operators'],
                   min_max=data['min_max'],
                   objective=data['objective'],
                   solution=solution)

    return solution
