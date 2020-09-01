from math import comb
from scipy.special import factorial


def stirling(n, k):
    stirling_number = 0
    for i in range(k + 1):
        stirling_number += ((-1)**i) * comb(k, i) * ((k-i)**n)
    return stirling_number * 1.0 / factorial(k, True)