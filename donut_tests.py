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

import csv

import numpy
import json

import argparse
import matplotlib.pyplot
import scipy.stats
parser = argparse.ArgumentParser(description='Test data for distinguishability form random, using NIST SP800-22Rev1a algorithms.')
parser.add_argument('alphabet_size', type=int, help='Size of alphabet to consider')
parser.add_argument('filename', type=str, nargs='?', help='Filename of binary file to test')
parser.add_argument('-t', '--testname', default=None,help='Select the test to run. Defaults to running all tests. Use --list_tests to see the list')
parser.add_argument('--list_tests', action='store_true',help='Display the list of tests')
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

config = []
with open(config_path) as config_payload:
    config = json.load(config_payload)

# with open(filename, 'r') as source:
#     reader = csv.reader(source)
#     for row in reader:
#         data = row[0]
#         stuff = data.split(";")
#         if stuff[0] != '0':
#             number = stuff[2]
#             dest.write(number)
#             dest.write("\n")

m = __import__("donut_" + test + "_test")
func = getattr(m, test + "_test")
p_values = []
for i in range(0, 10000):
    print(i)
    arr = numpy.random.randint(0, sigma, 100000)
    (success,p,plist) = func(arr, sigma, config[test])
    p_values.append(p)

matplotlib.pyplot.hist(p_values, 10)
matplotlib.pyplot.show()
statistic, kspvalue = scipy.stats.kstest(p_values, 'uniform')
print(kspvalue)
