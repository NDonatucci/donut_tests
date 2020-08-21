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
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *
from scipy.stats import chisquare, kstest
import numpy as np
import random

def countBlockAppearances(arr, pattern):
    position = 0
    count = 0
    pattern = list(pattern)
    m = len(pattern)
    while position < (len(arr)-m):
        if np.array_equal(arr[position:position+m], pattern):
            position += m
            count += 1
        else:
            position += 1
    return count

def non_overlapping_template_matching_test(arr, sigma):
    # Need to generate aperiodic pattern of length, of alphabet sigma.
    n = len(arr)

    B = [0,1,1] # pattern
    m = len(B)
    
    N = 8
    M = int(math.floor(n/8))
    n = M*N
    block_size = M

    randomVariables = list()
    for i in range(N):
        block = arr[i*block_size:((i+1)*block_size)]
        randomVariables.append(countBlockAppearances(block, B))

    expectedValue = float(M-m+1)/float(sigma**m)

    chisq, p = chisquare(randomVariables, [expectedValue] * N, 0, None)

    success = ( p >= 0.01)
    return (success,p,None)
