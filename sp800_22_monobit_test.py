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
import matplotlib.pyplot
from fractions import Fraction

from scipy.stats import chisquare, kstest
from gamma_functions import *


def countVars(block, sigma):
    count = [0] * sigma
    for i in block:
        count[i] = count[i] + 1
    return count

def monobit_test(arr, sigma):
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    n = len(arr)

    if len(arr) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return False,1.0,None

    expectedValue = n * 1.0/sigma
    randomVariables = countVars(arr, sigma)


    chisq, p = chisquare(randomVariables, [expectedValue] * sigma, 0, None)

    success = (p >= 0.01)
    return success, p, None


