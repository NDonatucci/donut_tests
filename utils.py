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


def collapse_categories_left(probs, vars, samples_num, magic_number):
    collapsed_probs = []
    collapsed_vars = []
    accum_prob = 0
    index = 0

    for i in probs:
        accum_prob += i
        exp_samples = accum_prob*samples_num
        if exp_samples >= magic_number:
            break
        index+=1

    collapsed_probs.append(accum_prob)
    collapsed_vars.append(sum(vars[0:index+1]))
    for i in range(index+1, len(probs)):
        collapsed_probs.append(probs[i])
        collapsed_vars.append(vars[i])

    return collapsed_probs, collapsed_vars


def collapse_categories_right(probs, vars, samples_num, magic_number):
    collapsed_probs = []
    collapsed_vars = []
    accum_prob = 0
    index = 0

    for i in range(len(probs)-1, -1, -1):
        accum_prob += probs[i]
        exp_samples = accum_prob*samples_num
        if exp_samples >= magic_number:
            index = i
            break

    for i in range(0, index):
        collapsed_probs.append(probs[i])
        collapsed_vars.append(vars[i])
    collapsed_probs.append(accum_prob)
    collapsed_vars.append(sum(vars[index:len(vars)]))

    return collapsed_probs, collapsed_vars


def collapse_categories(probs, vars, samples_num, magic_number):
    leftProbs, leftVars = collapse_categories_left(probs, vars, samples_num, magic_number)
    rightPorbs, rightVars = collapse_categories_right(leftProbs, leftVars, samples_num, magic_number)
    return rightPorbs, rightVars
