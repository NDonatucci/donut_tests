#!/usr/bin/env python

from __future__ import print_function

from scipy.stats import chisquare


def count_vars(block, sigma):
    count = [0] * sigma
    for i in block:
        count[i] = count[i] + 1
    return count


# At least n=100 recommended
def monobit_test(arr, sigma, params):
    n = len(arr)

    expected_value = n * 1.0 / sigma
    random_variables = count_vars(arr, sigma)

    chisq, p = chisquare(random_variables, [expected_value] * sigma, 0, None)

    success = (p >= 0.01)
    return success, p, None
