#!/usr/bin/env python

# sp800_22_tests.py
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

import json

import argparse
import pandas as pd
import results

parser = argparse.ArgumentParser(description='Test data for distinguishability form random, using NIST SP800-22Rev1a algorithms.')
parser.add_argument('alphabet_size', type=int, help='Size of alphabet to consider')
parser.add_argument('filename', type=str, nargs='?', help='Filename of binary file to test')
parser.add_argument('-t', '--testname', default=None,help='Select the test to run. Defaults to running all tests. Use --list_tests to see the list')
parser.add_argument('--mode', default="default", type=str)
parser.add_argument('--test', default="monobit", type=str)
parser.add_argument('--config', default="config.json", type=str)
parser.add_argument('--stream_size', default=10000, type=int)

args = parser.parse_args()

filename = args.filename
sigma = args.alphabet_size
test = args.test
config_path = args.config
stream_size = args.stream_size


def get_numbers(block):
    res = []
    for index, row in block.iterrows():
        res.append(int(row[0]))
    return res


config = {}
with open(config_path) as config_payload:
    config = json.load(config_payload)

significance_level = config["significance_level"]

# Run a whole test
for test in config["tests"]:
    m = __import__("donut_" + test + "_test")
    func = getattr(m, test + "_test")
    p_values = []

    for chunk in pd.read_csv(filename, chunksize=stream_size, header=None):
        arr = get_numbers(chunk)
        if (len(arr) == stream_size):
            (success,p,plist) = func(arr, sigma, config["configs"][test], significance_level)
            p_values.append(p)
    results.report_test(p_values, test, significance_level)
