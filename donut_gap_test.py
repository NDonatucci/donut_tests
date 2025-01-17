#!/usr/bin/env python

from __future__ import print_function

import math

from scipy.stats import chisquare


def convert_to_float(nums, base):
    res = 0
    for i in range(len(nums)):
        exp = (-(i+1))
        res += nums[i] * (base**exp)
    return res


def transform_input(numbers, base, block_size):
    res = []
    num_of_blocks = int(math.floor(len(numbers)/block_size))
    for i in range(num_of_blocks):
        block = numbers[i*block_size:((i+1)*block_size)]
        res.append(convert_to_float(block, base))
    return res


def get_gaps(arr, alpha, beta):
    gaps = []
    r = 0
    for i in range(len(arr)):
        if alpha <= arr[i] < beta:
            gaps.append(r)
            r = 0
        else:
            r += 1
    return gaps


def find_t(p, n):
    suma = 0
    for t in range(n):
        suma += p*(1-p)**t
        if suma >= 0.95:
            return t
    return 10


def get_histogram(gaps, t):
    buckets = [0] * (t + 1)
    for gap in gaps:
        if gap >= t:
            buckets[t] += 1
        else:
            buckets[gap] += 1
    return buckets


def generate_probabilities(p, t):
    probabilities = list()
    for r in range(t):
        probabilities.append(p*(1-p)**r)
    probabilities.append((1-p)**t)
    return probabilities


# Alpha = Lower end of interval
# Beta = Higher end of interval
# m = How many integers to use for a single float
# t = Gap size after which categories will be collapsed
def gap_test(arr, sigma, params, significance_level):
    m = params["m"] if "m" in params else 5
    alpha = params["alpha"] if "alpha" in params else 1/3
    beta = params["beta"] if "beta" in params else 2/3

    float_arr = transform_input(arr, sigma, m)
    gaps = get_gaps(float_arr, alpha, beta)
    n = len(gaps)

    t = params["t"] if "t" in params else find_t(beta - alpha, n)

    histogram = get_histogram(gaps, t)
    probabilities = generate_probabilities(beta - alpha, t)
    expected_values = list(map(lambda x: x * n, probabilities))
    p = 0
    if sum(expected_values) != 0 and sum(probabilities) != 0:
        chisq, p = chisquare(histogram, expected_values, 0, None)
    if math.isnan(p):
        p = 0

    success = (p >= significance_level)
    return success, p, None

