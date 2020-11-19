#!/usr/bin/env python

# sp800_22_frequency_within_block_test.pylon
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


def gap_test(arr, sigma):
    float_arr = transform_input(arr, sigma, 5)  # block size?
    alpha = 1/3
    beta = 2/3  # frutita estos numeros

    gaps = get_gaps(float_arr, alpha, beta)
    n = len(gaps)
    t = find_t(beta - alpha, n)
    histogram = get_histogram(gaps, t)
    probabilities = generate_probabilities(beta - alpha, t)
    expected_values = list(map(lambda x: x * n, probabilities))

    chisq, p = chisquare(histogram, expected_values, 0, None)

    success = (p >= 0.01)
    return success, p, None

