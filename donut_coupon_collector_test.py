#!/usr/bin/env python

from __future__ import print_function

import math

from utils import stirling
from scipy.special import factorial
from scipy.stats import chisquare


def get_histogram(coupons, sigma, t):
    buckets = [0] * (t + 1)
    for coupon in coupons:
        if coupon >= t:
            buckets[t] += 1
        else:
            buckets[coupon] += 1
    return buckets[sigma:t + 1]


def get_album_sizes(arr, sigma):
    d = dict()
    coupons = list()
    distinct = 0
    count = 0
    for elem in arr:
        count +=1
        if elem not in d:
            d[elem] = 1
            distinct += 1
            if distinct == sigma:
                d = dict()
                distinct = 0
                coupons.append(count)
                count = 0
    return coupons


def generate_probabilities(sigma, t):
    probabilities = list()
    for r in range(sigma, t):
        probabilities.append(float(factorial(sigma, True)) / float(sigma**r) * stirling(r - 1, sigma - 1))
    probabilities.append(1 - (factorial(sigma, True)/sigma**(t-1))*stirling(t-1, sigma))
    return probabilities


def find_t(sigma, n):
    t = sigma
    tail = 10
    while tail >= 5:
        tail = n * (1 - (factorial(sigma, True)/sigma**(t-1))*stirling(t-1, sigma))
        t += 1
    return t


# t = Album size after which all categories will be collapsed.
def coupon_collector_test(arr, sigma, params):
    album_sizes = get_album_sizes(arr, sigma)
    n = len(album_sizes)

    t = params["t"] if "t" in params else find_t(sigma, n)

    histogram = get_histogram(album_sizes, sigma, t)
    probabilities = generate_probabilities(sigma, t)
    expected_values = list(map(lambda x: x * n, probabilities))

    chisq, p = chisquare(histogram, expected_values, 0, None)
    if math.isnan(p):
        p = 0

    success = (p >= 0.01)
    return success, p, None
