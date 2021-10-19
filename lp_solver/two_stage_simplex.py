import numpy as np
import random

from utils.print_utils import print_colored


class TwoStageSimplex:
    def __init__(self, constraints, terms, operators, objective, min_max):
        assert min_max == 'max' or min_max == 'min', 'min_max can be \'max\' or \'min\''
        self.constraints = constraints
        self.terms = terms
        self.operators = operators
        self.objective = objective
        self.min_max = min_max
        self._max_iterations = len(constraints) * 2

        print_colored('---TWO-STAGE SIMPLEX---', 'cyan')
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

    def solve(self):
        iterations = 0
        self.n_variables = len(self.constraints[0])
        self._convert_equalities()
        self._init_tableau()

        print_colored('---FIRST STAGE---', 'y')
        self._first_stage = True
        while True:
            if iterations > self._max_iterations:
                return None
            p_row, p_col = self._loc_pivot()
            if p_row == -1:
                return np.inf
            if p_row is None:
                if self._first_stage:
                    if self._last_row[-1] != 0:
                        return None  # no feasible solution
                    self._first_stage = False
                    # go to second stage: remove last row and artificial columns
                    self._tab = self._tab[:-1]
                    first_a_index = self.n_variables + len(self.constraints)
                    last_a_index = len(self._tab[0]) - 1
                    self._tab = np.delete(self._tab, np.s_[first_a_index:last_a_index], axis=1)

                    self._values = self._tab[:, -1]
                    self._last_row = self._tab[-1]
                    print_colored('---SECOND STAGE---', 'y')
                    print(self._tab)
                else:
                    break
            else:
                self._update_associations(p_row, p_col)
                self._pivot_operation(p_row, p_col)
            iterations += 1

        return self._construct_solution()

    def _init_tableau(self):
        self._lts = np.count_nonzero(self.operators == '<=')
        self._gts = np.count_nonzero(self.operators == '>=')

        # one for each constraint + one for Q + one for I
        self._nrows = len(self.constraints) + 2
        # one for each variable + one for each slack and surplus variable (one for each constraint) + one for each >= + one for the final term
        self._ncolumns = self.n_variables + len(self.constraints) + self._gts + 1
        self._tab = np.zeros((self._nrows, self._ncolumns))
        self._values = self._tab[:, -1]
        self._last_row = self._tab[-1]

        # for each constraint put its values into the tableau
        for i in range(len(self.constraints)):
            constraint = self.constraints[i]
            tab_row = self._tab[i]
            # copy variables coefficients
            for j in range(len(constraint)):
                tab_row[j] = constraint[j]

            assert self.operators[i] == '<=' or self.operators[i] == '>='
            if self.operators[i] == '<=':
                # slack variable
                tab_row[self.n_variables + i] = 1
            else:
                # surplus variable
                tab_row[self.n_variables + i] = -1
                # artificial variable
                # gt_index = self.operators[:i].count('>=')
                gt_index = np.count_nonzero(self.operators[:i] == '>=')
                tab_row[self.n_variables + len(self.constraints) + gt_index] = 1
                # one in the last row corresponding to the surplus variable
                self._last_row[self.n_variables + i] = 1

            # copy term
            tab_row[-1] = self.terms[i]

        # put the real objective function into the tableau
        second_last_row = self._tab[-2]
        for j in range(len(self.objective)):
            second_last_row[j] = -self.objective[j] if self.min_max == 'max' else self.objective[j]

        # put the temporary objective function into the tableau
        # filter only >= constraints
        gt_constraints = []
        gt_values = []
        for constraint, value, operator in zip(self.constraints, self.terms, self.operators):
            if operator == '>=':
                gt_constraints.append(constraint)
                gt_values.append(value)
        gt_constraints = np.array(gt_constraints)
        gt_values = np.array(gt_values)
        # first n_variables elements are the negated sum of variables
        self._last_row[:self.n_variables] = np.negative(np.sum(gt_constraints, axis=0))
        # value is the negated sum of values
        self._last_row[-1] = np.negative(np.sum(gt_values))

        print_colored('---TABLEAU INITIALIZED---', 'y')
        print(self._tab)

        self._init_associations()

    def _init_associations(self):
        self._associations = dict()

    def _loc_pivot(self):
        # pivot column = minimum negative value index of last row
        col_index = np.argmin(self._last_row[:-1])  # except the value column

        # if the minimum of the last row is non negative
        if self._last_row[col_index] >= 0:
            return None, None

        col = self._tab[:, col_index]

        # theta values computation
        with np.errstate(divide='ignore', invalid='ignore'):
            theta = np.divide(self._values, col)[:-1]
            if self._first_stage:
                theta = np.divide(self._values, col)[:-2]  # except last two rows
            else:
                theta = np.divide(self._values, col)[:-1]  # except last row
            print('THETA {}', theta)

        # pivot row = minimum positive theta index
        positives = theta[(theta >= 0) & (theta != np.inf) & (theta != np.nan)]  # ***>=***
        if len(positives) == 0:
            return -1, -1

        min_positive = min(positives)
        indexes = []
        for i in range(len(theta)):
            if theta[i] == min_positive:
                indexes.append(i)

        # row_index = list(theta).index(min(positives))
        row_index = random.choice(indexes)

        print('PIVOT ROW {} COLUMN {}'.format(row_index, col_index))

        return row_index, col_index

    def _update_associations(self, p_row, p_col):
        self._associations[p_col] = p_row
        print('Associations updated {}'.format(self._associations))

    def _pivot_operation(self, p_row, p_col):
        pivot = self._tab[p_row, p_col]
        pivot_row = self._tab[p_row]
        self._update_pivot_row(pivot, p_row)

        for i in range(len(self._tab)):
            if i != p_row:
                self._tab[i] = self._tab[i] - self._tab[i][p_col] * pivot_row

        print_colored('---PIVOTED---', 'y')
        print(self._tab)

    def _update_pivot_row(self, pivot, p_row):
        self._tab[p_row] = np.divide(self._tab[p_row], pivot)

    def _construct_solution(self):
        solution = dict()

        print(self._associations)
        for i in range(self.n_variables):
            index = self._associations.get(i)
            solution['x' + str(i)] = self._tab[index, -1] if index is not None else 0
        solution['objective'] = self._tab[-1, -1] if self.min_max == 'max' else -self._tab[-1, -1]

        print_colored('---CONSTRUCTED SOLUTION---', 'g')
        print(solution)

        return solution

    def _convert_equalities(self):
        for i in range(len(self.operators)):
            assert self.operators[i] == '<=' or self.operators[i] == '>=' or self.operators[i] == '='
            if self.operators[i] == '=':
                self.operators[i] = '<='
                self.operators = np.append(self.operators, '>=')
                self.constraints = np.append(self.constraints, [self.constraints[i].copy()], axis=0)
                self.terms = np.append(self.terms, self.terms[i])
