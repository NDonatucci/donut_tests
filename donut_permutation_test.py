#!/usr/bin/env python

from __future__ import print_function

from scipy.stats import chisquare
from scipy.special import factorial
import numpy as np
import math


def swap(arr, r, s):
    tmp = arr[r]
    arr[r] = arr[s]
    arr[s] = tmp
    return arr


def analise_permutation(block, t):
    r = t
    f = 0
    while r > 1:
        sub_block = block[0:r]
        max_item = max(sub_block)
        s = np.where(sub_block == max_item)[0][0]
        f = r * f + s
        block = swap(block, r - 1, s)
        r -= 1
    return f


def get_permutations(arr, t):
    t_fact = factorial(t, True)
    number_of_blocks = math.floor(len(arr)/t)
    res = [0] * t_fact
    for i in range(number_of_blocks):
        f = analise_permutation(arr[i*t:(i+1)*t], t)
        res[f] += 1
    return res


# t = word length
def permutation_test(arr, sigma):
    t = 5
    t_fact = factorial(t, True)
    random_variables = get_permutations(arr, t)
    number_of_blocks = math.floor(len(arr)/t)
    expected_values = [number_of_blocks/t_fact] * t_fact

    chisq, p = chisquare(random_variables, expected_values, 0, None)

    success = (p >= 0.01)
    return success, p, None
