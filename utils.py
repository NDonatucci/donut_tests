from math import comb
from scipy.special import factorial

stirling_dict = {}


def stirling(n, k):
    if (n, k) in stirling_dict:
        return stirling_dict[(n, k)]
    else:
        stirling_number = 0
        for i in range(k + 1):
            stirling_number += ((-1) ** i) * comb(k, i) * ((k - i) ** n)
        res = stirling_number * 1.0 / factorial(k, True)
        stirling_dict[(n, k)] = res
        return res
