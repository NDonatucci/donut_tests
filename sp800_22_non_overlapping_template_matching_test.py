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
from collections import defaultdict
import random

def countBlockAppearances2(arr, pattern):
    position = 0
    count = 0
    pattern = list(pattern)
    m = len(pattern)
    while position <= (len(arr)-m):
        if np.array_equal(arr[position:position+m], pattern):
            count += 1
        position += m
    return count

def countBlockAppearances3(arr, pattern):
    count = [0,0,0,0]
    a = math.floor(len(arr)/2)
    for i in range(a):
        l = arr[i*2]
        r = arr[i*2 + 1]
        if l == 0 and r == 0:
            count[0]=count[0]+1
        elif l==0 and r==1:
            count[1]=count[1]+1
        elif l==1 and r==0:
            count[2]=count[2]+1
        else:
            count[3]=count[3]+1
    return count

def countBlockAppearances(arr, m, sigma):
    d = defaultdict(lambda: 0)
    for i in range(math.floor(len(arr)/m)):
        d["".join(map(str, arr[i*m:(i+1)*m]))]+=1
    listorti = list(d.values())
    longitud = sigma**m
    ble = len(listorti)
    listorti.extend([0]*(longitud - ble))
    return listorti


def non_overlapping_template_matching_test(arr, sigma):
    n = len(arr)

    m = 3
    
    N = 99
    M = int(math.floor(n/N))
    n = M*N
    block_size = M

    expectedValue = float(M//m)/float(sigma**m)
    randomVariables = list()
    for i in range(N):
        block = arr[i*block_size:((i+1)*block_size)]
        randomVariables.extend(countBlockAppearances(block, m, sigma))

    chisq, p = chisquare(randomVariables, [expectedValue] * (N * sigma**m), N - 1, None)

    success = ( p >= 0.01)
    return (success,p,None)
