#!/usr/bin/env python

from __future__ import print_function

import math
from scipy.stats import chisquare
from collections import defaultdict


def count_block_appearances(arr, m, sigma):
    d = defaultdict(lambda: 0)
    for i in range(math.floor(len(arr)/m)):
        d["".join(map(str, arr[i*m:(i+1)*m]))] += 1
    listorti = list(d.values())
    number_of_words = sigma**m
    observed_words = len(listorti)
    listorti.extend([0]*(number_of_words - observed_words))
    return listorti


# no more than 99 blocks recommended
# m = length of pattern
# M = block size
def frequency_of_words_test(arr, sigma):
    n = len(arr)
    m = 3
    
    N = 99
    M = int(math.floor(n/N))
    block_size = M

    expected_value = float(M//m)/float(sigma**m)
    random_variables = list()
    for i in range(N):
        block = arr[i*block_size:((i+1)*block_size)]
        random_variables.extend(count_block_appearances(block, m, sigma))

    chisq, p = chisquare(random_variables, [expected_value] * (N * sigma**m), N - 1, None)

    success = (p >= 0.01)
    return success, p, None
