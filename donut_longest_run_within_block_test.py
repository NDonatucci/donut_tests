#!/usr/bin/env python

from __future__ import print_function

import math

from scipy.stats import chisquare


def get_d(matrix, sigma, n, k):
    if n==1 and k==0:
        return sigma-1
    if n==2 and k==0:
        return (sigma-1)**2
    if k==n-1:
        return 0
    if k==0:
        return (sigma-1)**n

    return matrix[n,k]


def calculate_d(n, sigma):
    matrix = dict()
    for nn in range(3, n+1, 1):
        for kk in range(nn-1):
            matrix[nn, kk] = 0
            for j in range(1, nn - kk + 1, 1):
                for s in range(0, min(kk-1, j-2)+1, 1):
                    for t in range(0, min(kk, nn-j-kk)+1, 1):
                        matrix[nn,kk]=matrix[nn,kk]+get_d(matrix, sigma, j-1, s)*get_d(matrix, sigma, nn-j+1-kk, t)
    res = list()
    for kk in range(n):
        res.append(get_d(matrix, sigma, n, kk))
    return res


def count_longest_run(block, t):
    longest_run = 0
    run = 0
    for i in range(0, len(block)):
        if block[i] == t:
            run+=1
        else:
            if run > longest_run:
                longest_run = run
            run=0
        if i == len(block) - 1:
            if run > longest_run:
                longest_run = run
    return longest_run


def collapse_categories(arr, index):
    res = list()
    res.extend(arr[0:index])
    suma = 0
    for i in range(index, len(arr)):
        suma += arr[i]
    res.append(suma)
    return res


# t = Given character of the alphabet
# m = Block Size
# algo pal colapso de la cola?
def longest_run_within_block_test(arr, sigma):
    t = 0
    n = len(arr)
    block_size = 40
    d_list = calculate_d(block_size + 2, sigma)
    probs = [0] * block_size
    for i in range(0, len(probs)):
        probs[i] = (d_list[i] // (sigma-1)**2) / sigma**block_size

    num_of_blocks = int(math.floor(n/block_size))

    random_variables = [0] * block_size
    for i in range(num_of_blocks):
        block = arr[i*block_size:((i+1)*block_size)]
        run = count_longest_run(block, t)
        random_variables[run]+=1

    suma = 0
    index = 0
    for i in range(0, len(probs)):
        suma += probs[i]
        if suma >= 0.99:
            index = i
            break

    random_variables = collapse_categories(random_variables, index)
    probs = collapse_categories(probs, index)

    chisq, p = chisquare(random_variables, [i * num_of_blocks for i in probs], 0, None)

    success = (p >= 0.01)
    if not success:
        print(random_variables)
        print([i * num_of_blocks for i in probs])
    return success, p, None
