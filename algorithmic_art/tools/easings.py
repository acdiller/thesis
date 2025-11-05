"""
Assortment of easing functions.
"""
import math


def linear(x):
    return x


def quad_in(x):
    return x * x


def quad_out(x):
    return -x * (x- 2)


def quad_inout(x):
    return (2 * x * x) if x < 0.5 else (-2 * x * (x - 2) - 1)


def cubic_in(x):
    return x * x * x


def cubic_out(x):
    return (x - 1) ** 3 + 1


def cubic_inout(x):
    return (4 * x * x * x) if x < 0.5 else (4 * (x - 1) ** 3 + 1)


def sine_in(x):
    return 1 - math.cos(x * math.pi / 2)


def sine_out(x):
    return math.sin(x * math.pi / 2)


def sin_inout(x):
    return -(math.cos(x * math.pi) - 1) / 2


def exp_in(x, a=10):
    return 2 ** (a * (x - 1))


def exp_out(x, a=10):
    return 1 - 2 ** (-a * x)


def exp_inout(x, a=10):
    if x < 0.5:
        return (2 ** (a * (2 * x - 1))) / 2
    else: 
        return 1 - 2 ** (a * (1 - 2 * x) - 1)


def circ_in(x):
    return -(math.sqrt(1 - x * x) - 1)


def circ_out(x):
    return math.sqrt(-x * (x - 2))


def circ_inout(x):
    if x < 0.5:
        return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
    else:
        return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2