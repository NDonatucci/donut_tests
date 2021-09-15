#!/usr/bin/env python

from __future__ import print_function

import math

from scipy.stats import chisquare


def count_block_vars(block, sigma):
    count = [0] * sigma
    for i in block:
        count[i] = count[i] + 1
    return count


# At least n=100 recommended
# No more than 99 blocks recommended
# M = Block Size
def frequency_within_block_test(arr, sigma, params, significance_level):
    n = len(arr)
    block_size = params["block_size"] if "block_size" in params else int(math.floor(n/99))
    num_of_blocks = int(math.floor(n/block_size))

    expected_value = block_size * 1.0/sigma
    random_variables = list()
    for i in range(num_of_blocks):
        block = arr[i*block_size:((i+1)*block_size)]
        block_vars = count_block_vars(block, sigma)
        random_variables.extend(block_vars)

    chisq, p = chisquare(random_variables, [expected_value] * (num_of_blocks * sigma), num_of_blocks - 1, None)

    success = (p >= significance_level)
    return success, p, None
