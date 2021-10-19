import math
import numpy as np


def is_integer_num(num):
    if isinstance(num, int):
        return True
    if isinstance(num, float):
        return num.is_integer()
    return False


def integer_bounds(num):
    return math.floor(num), math.ceil(num)
