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
def frequency_within_block_test(arr, sigma):
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    # miniumum block size 20 bits, most blocks 100
    n = len(arr)
    M = 20
    N = int(math.floor(n/M))
    if N > 99:
        N=99
        M = int(math.floor(n/N))

    num_of_blocks = N
    block_size = M

    expected_value = M * 1.0/sigma
    random_variables = list()
    for i in range(num_of_blocks):
        block = arr[i*block_size:((i+1)*block_size)]
        block_vars = count_block_vars(block, sigma)
        random_variables.extend(block_vars)

    chisq, p = chisquare(random_variables, [expected_value] * (N * sigma), N - 1, None)

    success = (p >= 0.01)
    return success, p, None
