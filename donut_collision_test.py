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


def calculate_percentage_points(m, n):
    array = []
    A = [0] * (n+1)
    A[1] = 1
    j0 = 1
    j1 = 1
    treshold = 10**-20
    for i in range(n-1):
        j1 += 1
        for j in range(j1, j0-1, -1):   # revisar
            A[j] = (j/m)*A[j] + ((1 + 1/m) - (j/m))*A[j-1]
            if A[j] < treshold:
                A[j] = 0
                if j == j1:
                    j1 -= 1
                if j == j0:
                    j0 += 1

    T = [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1.00]
    p = 0
    t = 0
    j = j0 - 1
    while T[t] != 1.00:
        j += 1
        p = p + A[j]
        if p > T[t]:
            array.append((1-p, n-j-1))
            # con probabilidad 1-p hay no mas de n - j - 1 colisiones
            while p > T[t]:
                t += 1
    print(array)
    return


def count_collisions(arr):
    collisions = 0
    d = {}
    for i in arr:
        if i in d:
            collisions+=1
        else:
            d[i] = 1
    return collisions


def collision_test(arr, sigma, params):
    calculate_percentage_points(sigma, len(arr))
    collisions = count_collisions(arr)
    print(collisions)

    success = True
    p = 0.03
    return success, p, None

