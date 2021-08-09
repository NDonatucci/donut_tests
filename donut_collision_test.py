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
import math


def calculate_percentage_points(m, n, points):
    array = []
    A = [0] * (n+1)
    A[1] = 1
    j0 = 1
    j1 = 1
    threshold = 10**-20
    for i in range(n-1):
        j1 += 1
        for j in range(j1, j0-1, -1):
            A[j] = (j/m)*A[j] + ((1 + 1/m) - (j/m))*A[j-1]
            if A[j] < threshold:
                A[j] = 0
                if j == j1:
                    j1 -= 1
                if j == j0:
                    j0 += 1

    p = 0
    t = 0
    j = j0 - 1
    while points[t] != 1.00:
        j += 1
        p = p + A[j]
        if p > points[t]:
            array.append((1-p, n-j-1))
            while p > points[t]:
                t += 1
    return array


def count_collisions(arr):
    collisions = 0
    d = {}
    for i in arr:
        if i in d:
            collisions+=1
        else:
            d[i] = 1
    return collisions


def transform_input(numbers, block_size):
    res = []
    num_of_blocks = int(math.floor(len(numbers)/block_size))
    for i in range(num_of_blocks):
        block = numbers[i*block_size:((i+1)*block_size)]
        res.append(convert(block))
    return res


def convert(block):
    s = ""
    for i in block:
        s = s + str(i)
    return int(s)


def get_expected(percentage_points, num_of_blocks):
    exp = [0] * (len(percentage_points) + 1)
    exp[0] = 1 - percentage_points[0][0]
    for i in range(1,len(percentage_points)):
        exp[i] = percentage_points[i-1][0] - percentage_points[i][0]
    exp[len(percentage_points)] = percentage_points[len(percentage_points) - 1][0]
    return [num_of_blocks*x for x in exp]


def get_histogram(percentage_points, collisions):
    histogram = [0] * (len(percentage_points) + 1)
    for col in collisions:
        histogram[get_bucket(percentage_points, col)] += 1
    return histogram


def get_bucket(percentage_points, col):
    for j in range(len(percentage_points)):
        if col > percentage_points[j][1]:
            return j
    return len(percentage_points)


def collision_test(arr, sigma, params):
    block_size = params["block_size"] if "block_size" in params else 1000
    m = params["m"] if "m" in params else 5
    points = params["percentage_points"] if "percentage_points" in params else [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1.00]
    collisions = []
    arr = transform_input(arr, m)
    num_of_blocks = int(math.floor(len(arr)/block_size))
    percentage_points = calculate_percentage_points(sigma**m, block_size, points)
    expected = get_expected(percentage_points, num_of_blocks)

    for i in range(num_of_blocks):
        block = arr[i*block_size:((i+1)*block_size)]
        collision = count_collisions(block)
        collisions.append(collision)

    histogram = get_histogram(percentage_points, collisions)

    chisq, p = chisquare(histogram, expected, 0, None)
    success = (p >= 0.01)
    return success, p, None

