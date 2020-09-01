#!/usr/bin/env python

# sp800_22_overlapping_template_mathcing_test.py
# 
# Copyright (C) 2017 David Johnston
# This program is distributed under the terms of the GNU General Public License.
# 
# This file is part of sp800_22_tests.
# 
# sp800_22_tests is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# sp800_22_tests is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with sp800_22_tests.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

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


def get_coupons(arr, sigma):
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


def coupon_collector_test(arr, sigma):
    coupons = get_coupons(arr, sigma)
    n = len(coupons)
    t = find_t(sigma, n)
    histogram = get_histogram(coupons, sigma, t)
    probabilities = generate_probabilities(sigma, t)
    expected_values = list(map(lambda x: x * n, probabilities))

    chisq, p = chisquare(histogram, expected_values, 0, None)

    success = (p >= 0.01)
    return success, p, None
