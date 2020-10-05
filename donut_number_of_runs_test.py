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

from scipy.stats import norm
from statsmodels.stats.weightstats import ztest
import math


def get_number_of_runs(arr):
    runs = 0
    for i in range(len(arr) - 1):
        if arr[i] != arr[i+1]:
            runs += 1
    return runs



def count_vars(arr, sigma):
    res = [0] * sigma
    for i in range(len(arr)):
        res[arr[i]] += 1
    return res


def get_mu(number_of_characters, n):
    sum = 0
    for nj in number_of_characters:
        sum += nj**2
    return (n * (n + 1) - sum) / n


def get_stddev(number_of_characters, n):
    squareSum = 0
    cubicSum = 0
    for nj in number_of_characters:
        squareSum += nj**2
        cubicSum += nj**3
    numerator = squareSum * (squareSum + n * (n+1)) - 2 * n * cubicSum - n**3
    denominator = n**2 * (n+1)
    return math.sqrt(numerator/denominator)


def get_z(r, mu, stddev):
    if r >= mu:
        return (r - mu - 0.5) / stddev
    else:
        return (r - mu + 0.5) / stddev


def number_of_runs_test(arr, sigma):
    number_of_characters = count_vars(arr, sigma)
    n = len(arr)
    mu = get_mu(number_of_characters, n)
    stddev = get_stddev(number_of_characters, n)
    number_of_runs = get_number_of_runs(arr)


    z = get_z(number_of_runs, mu, stddev)

    p = 2*(1 - norm.cdf(abs(z)))

    success = (p >= 0.01)
    return success, p, None
