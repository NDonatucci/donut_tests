#!/usr/bin/env python

# sp800_22_non_overlapping_template_matching_test.py
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
from collections import defaultdict


def count_block_appearances(arr, m, sigma):
    d = defaultdict(lambda: 0)
    for i in range(math.floor(len(arr)/m)):
        d["".join(map(str, arr[i*m:(i+1)*m]))] += 1
    listorti = list(d.values())
    longitud = sigma**m
    ble = len(listorti)
    listorti.extend([0]*(longitud - ble))
    return listorti


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
