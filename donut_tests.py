#!/usr/bin/env python

from __future__ import print_function

import json

import argparse
import results

parser = argparse.ArgumentParser(description='Test data for distinguishability form random')
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


def get_stream(file, offset, size):
    arr = []
    with open(file, "r") as input:
        input.seek(offset)
        for i in range(size):
            line = input.readline()
            line = line.rstrip()
            arr.append(int(line))
        stop = input.tell()
        return (arr, stop)


config = {}
with open(config_path) as config_payload:
    config = json.load(config_payload)

significance_level = config["significance_level"]

# Run a whole test
for test in config["tests"]:
    m = __import__("donut_" + test + "_test")
    func = getattr(m, test + "_test")
    p_values = []

    num_lines = sum(1 for line in open(filename))
    streams = num_lines//stream_size

    offset = 0
    for i in range(streams):
        (arr, position) = get_stream(filename, offset, stream_size)
        offset = position
        (success,p,plist) = func(arr, sigma, config["configs"][test], significance_level)
        p_values.append(p)
    results.report_test(p_values, test, significance_level)
