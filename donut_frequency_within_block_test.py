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


def count_block_vars(block, sigma):
    count = [0] * sigma
    for i in block:
        count[i] = count[i] + 1
    return count


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
    
    if len(arr) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return False,1.0,None

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
