import matplotlib.pyplot as plt
import numpy as np


def plot_2d_lp(constraints, terms, operators, min_max, objective, solution=None):
    x = np.linspace(-2, 7, 2)

    for i in range(len(constraints)):
        constraint = constraints[i]
        term = terms[i]

        y = (- constraint[0]/constraint[1]) * x + term/constraint[1]

        color = '-y'
        if operators[i] == '<=':
            color = '-b'
        elif operators[i] == '>=':
            color = '-r'
        elif operators[i] == '=':
            color = '-g'

        plt.plot(x, y, color, label='Constraint {} {}'.format(i, operators[i]))

    y = (- objective[0]/objective[1]) * x + term/objective[1]
    plt.plot(x, y, '-y', label='Objective')

    plt.plot(solution['x0'], solution['x1'], 'ro')
    plt.title(label=min_max)
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
