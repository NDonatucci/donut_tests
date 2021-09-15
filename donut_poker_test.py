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
from utils import stirling
from utils import collapse_categories
import math


def count_different(arr):
    return len(set(arr))


def get_hands(arr, hand_size):
    amount_of_hands = math.floor(len(arr)/hand_size)
    res = [0] * hand_size
    for i in range(amount_of_hands):
        different_cards = count_different(arr[i*hand_size:(i+1)*hand_size])
        res[different_cards - 1] += 1
    return res


def generate_probabilities(sigma, hand_size):
    res = [0] * hand_size
    for r in range(1, hand_size + 1):
        mult = sigma
        for i in range(1, r):
            mult = mult * (sigma - i)
        mult = mult / (sigma**hand_size)
        res[r - 1] = mult * stirling(hand_size, r)
    return res


# hand_size = Size of hand
def poker_test(arr, sigma, params, significance_level):
    hand_size = params["hand_size"] if "hand_size" in params else 5
    random_variables = get_hands(arr, hand_size)
    probabilities = generate_probabilities(sigma, hand_size)
    n = sum(random_variables)
    collapsed_probs, collapsed_vars = collapse_categories(probabilities, random_variables, n, 5)

    expected_values = list(map(lambda x: x * n, collapsed_probs))

    chisq, p = chisquare(collapsed_vars, expected_values, 0, None)

    success = (p >= significance_level)
    return success, p, None
