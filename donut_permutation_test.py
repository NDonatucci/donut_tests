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
        #s = sub_block.index(max_item)
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


def permutation_test(arr, sigma):
    t = 5
    t_fact = factorial(t, True)
    random_variables = get_permutations(arr, t)
    number_of_blocks = math.floor(len(arr)/t)
    expected_values = [number_of_blocks/t_fact] * t_fact

    chisq, p = chisquare(random_variables, expected_values, 0, None)

    success = (p >= 0.01)
    return success, p, None
