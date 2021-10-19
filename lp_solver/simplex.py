import numpy as np


class Simplex:
    def __init__(self, constraints, terms, operators, objective, min_max):
        assert min_max == 'max' or min_max == 'min', 'min_max can be \'max\' or \'min\''
        self.constraints = constraints
        self.terms = terms
        self.operators = operators
        self.objective = objective
        self.min_max = min_max

        print('---PROBLEM DEFINITION---')
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
        self._init_tableau()
        while True:
            p_row, p_col = self._loc_pivot()
            if p_row is None:
                break
            self._update_associations(p_row, p_col)
            self._pivot_operation(p_row, p_col)
        return self._construct_solution()

    def _init_tableau(self):
        self._nrows = len(self.constraints) + 1
        self._ncolumns = len(self.constraints[0]) + len(
            self.constraints) + 1  # one for each variable + one for each slack variable + one for the final term
        self._tab = np.zeros((self._nrows, self._ncolumns))
        self._values = self._tab[:, -1]

        # for each constraint put its values into the tableau
        for i in range(len(self.constraints)):
            constraint = self.constraints[i]
            tab_row = self._tab[i]
            # copy variables coefficients
            for j in range(len(constraint)):
                tab_row[j] = constraint[j]

            # slack variable
            tab_row[len(self.constraints[0]) + i] = 1  # TODO: check '[0]'

            # copy term
            tab_row[-1] = self.terms[i]

        # put the objective function into the tableau
        self._last_row = self._tab[-1]
        for j in range(len(self.objective)):
            self._last_row[j] = -self.objective[j] if self.min_max == 'max' else self.objective[j]

        print('---TABLEAU INITIALIZED---')
        print(self._tab)

        self._init_associations()

    def _init_associations(self):
        self._associations = dict()
        # for i in range(len(self.constraints)):
        #     self._associations[i] = ('slack_' + str(i))
        #
        # print('ASSOCIATIONS {}'.format(self._associations))

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

        print('THETA {}'.format(theta))

        # pivot row = minimum positive theta index
        row_index = list(theta).index(min(theta[theta >= 0]))  # ***>=***

        print('PIVOT ROW {} COLUMN {}'.format(row_index, col_index))

        return row_index, col_index

    def _update_associations(self, p_row, p_col):
        # self._associations[p_row] = 'x' + str(p_col)
        self._associations[p_col] = p_row
        print('Associations updated {}'.format(self._associations))

    def _pivot_operation(self, p_row, p_col):
        pivot = self._tab[p_row, p_col]
        pivot_row = self._tab[p_row]
        self._update_pivot_row(pivot, p_row)

        for i in range(len(self._tab)):
            if i != p_row:
                # self._tab[i] = [el - self._tab[i][p_col] * pivot_row[i] for el in self._tab[i]]
                self._tab[i] = self._tab[i] - self._tab[i][p_col] * pivot_row

        print('---PIVOTED---')
        print(self._tab)

    def _update_pivot_row(self, pivot, p_row):
        self._tab[p_row] = np.divide(self._tab[p_row], pivot)

        print('Pivot row updated')
        print(self._tab)

    def _construct_solution(self):
        solution = dict()

        # for key, value in self._associations.items():
        #     solution['x'+str(key)] = self._tab[key, -1]
        # solution['objective'] = self._tab[-1, -1]

        print(self._associations)
        for i in range(len(self.constraints[0])):
            index = self._associations.get(i)
            solution['x' + str(i)] = self._tab[index, -1] if index is not None else 0
        solution['objective'] = self._tab[-1, -1] if self.min_max == 'max' else -self._tab[-1, -1]

        print('---CONSTRUCTED SOLUTION---')
        print(solution)

        return solution
