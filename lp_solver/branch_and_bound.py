import numpy as np

from utils.number_utils import is_integer_num, integer_bounds
from utils.print_utils import print_colored
from utils.solution_utils import all_integers, solution_is_better, first_non_integer


class BranchAndBound:
    def __init__(self, constraints, terms, operators, objective, min_max, lp_solver):
        self.constraints = constraints
        self.terms = terms
        self.operators = operators
        self.objective = objective
        self.min_max = min_max
        self.lp_solver = lp_solver
        self.n_variables = len(constraints[0])
        # self.lp_solver = lp_solver(constraints, terms, operators, objective, min_max)

        print_colored('---BRANCH AND BOUND---', 'cyan')
        print('CONSTRAINTS')
        print(self.constraints)
        print('TERMS')
        print(self.terms)
        print('OPERATORS')
        print(self.operators)
        print('OBJECTIVE')
        print(self.objective)
        print('MIN_MAX')
        print(self.min_max)

    # def solve(self):
    #     current_constraints = self.constraints.copy()
    #     current_terms = self.terms.copy()
    #     current_operators = self.operators.copy()
    #
    #     best_solution = None
    #     while True:
    #         current_solution = self._construct_solution(current_constraints, current_terms, current_operators)
    #         if all_integers(current_solution):
    #             if solution_is_better(current_solution, best_solution):
    #                 best_solution = current_solution
    #         else:
    #             variable, value = first_non_integer(current_solution)
    #             first_branch, second_branch = self._branch_on_value(constraints=current_constraints,
    #                                                                 terms=current_terms,
    #                                                                 operators=current_operators,
    #                                                                 variable=variable,
    #                                                                 value=value)

    def solve(self):
        self._best_solution = None
        return self._explore_tree(self.constraints, self.terms, self.operators)

    def _explore_tree(self, constraints, terms, operators):
        current_constraints = constraints.copy()
        current_terms = terms.copy()
        current_operators = operators.copy()

        current_solution = self._construct_solution(current_constraints, current_terms, current_operators)

        if current_solution is None or current_solution is np.inf:
            return None
        if all_integers(current_solution):
            if solution_is_better(current_solution, self._best_solution, self.min_max):
                self._best_solution = current_solution
            return current_solution
        else:
            if solution_is_better(self._best_solution, current_solution, self.min_max):
                return None

        print_colored('---EXPLORING SUBTREE---', 'dy')
        print(current_solution)

        variable, value = first_non_integer(current_solution)

        print('Branching on {} = {}'.format(variable, value))

        first_branch, second_branch = self._branch_on_value(constraints=current_constraints,
                                                            terms=current_terms,
                                                            operators=current_operators,
                                                            variable=variable,
                                                            value=value)

        first_branch_solution = self._explore_tree(constraints=first_branch[0],
                                                   terms=first_branch[1],
                                                   operators=first_branch[2])
        second_branch_solution = self._explore_tree(constraints=second_branch[0],
                                                    terms=second_branch[1],
                                                    operators=second_branch[2])

        if solution_is_better(first_branch_solution, second_branch_solution, self.min_max):
            return first_branch_solution
        else:
            return second_branch_solution

    def _construct_solution(self, constraints, terms, operators):
        solver = self.lp_solver(constraints, terms, operators, self.objective, self.min_max)
        return solver.solve()

    # def _update_constraints(self, constraints, terms, operators, solution):
    #     updated_constraints = constraints.copy()
    #     updated_terms = terms.copy()
    #     updated_operators = operators.copy()
    #     for variable, value in solution.items():
    #         if not is_integer_num(value):
    #             variable_index = int(variable[1:])
    #             row = np.zeros(self.n_variables)
    #             row[variable_index] = 1
    #             lb, ub = integer_bounds(value)
    #
    #             updated_terms = np.append(updated_terms, ['<=', '>='])  # OPERATORS
    #             updated_terms = np.append(updated_terms, [lb, ub])
    #             updated_constraints = np.append(updated_constraints, [row.copy(), row.copy()], axis=0)

    def _branch_on_value(self, constraints, terms, operators, variable, value):
        variable_index = int(variable[1:])
        row = np.zeros(self.n_variables)
        row[variable_index] = 1
        lb, ub = integer_bounds(value)

        low_operators = np.append(operators.copy(), '<=')
        up_operators = np.append(operators.copy(), '>=')
        low_terms = np.append(terms.copy(), lb)
        up_terms = np.append(terms.copy(), ub)
        low_constraints = np.append(constraints.copy(), [row.copy()], axis=0)
        up_constraints = np.append(constraints.copy(), [row.copy()], axis=0)

        return (low_constraints, low_terms, low_operators), (up_constraints, up_terms, up_operators)
