#!/usr/bin/env python

# sp800_22_overlapping_template_mathcing_test.py
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

from math import comb
from scipy.special import factorial
from gamma_functions import *
import numpy as np

from scipy.stats import chisquare

def getCouponList(arr, sigma, t):
    couponList = [0] * (t + 1)
    d = dict()
    distinct = 0
    count = 0
    for elem in arr:
        count +=1
        if elem not in d:
            d[elem] = 1
            distinct +=1
            if distinct == sigma:
                d = dict()
                distinct = 0
                if count >= t:
                    couponList[t]+=1
                else:
                    couponList[count] +=1
                count = 0
    return couponList[sigma:t + 1] #revisar esto


def generateProbabilities(sigma, t):
    probabilities = list()
    for r in range(sigma, t):
        dFact = factorial(sigma, True)
        dr = sigma**r
        divisionLoca = float(dFact) / float(dr)
        rogerSterling = sterling(r -1, sigma - 1)
        #print("Sterling: ", sigma -1, r-1, ": ", rogerSterling)
        probabilities.append(divisionLoca*rogerSterling)
    lastNumber = 1 - (factorial(sigma, True)/sigma**(t-1))*sterling(t-1,sigma)
    probabilities.append(lastNumber)
    return probabilities


def sterling(n, k):
    sum = 0
    for i in range(k + 1):
        sum += ((-1)**i)*comb(k,i)*((k-i)**n)
    return sum * 1.0/factorial(k, True)


def coupon_collector_test(arr, sigma):
    t = 5
    couponLengths = getCouponList(arr, sigma, t)
    if len(couponLengths) != t - sigma + 1:
        print("TUVIEJA")
    probabilities = generateProbabilities(sigma, t)
    amountOfCoupons = sum(couponLengths)
    expectedValues = list(map(lambda x: x * amountOfCoupons, probabilities))

    chisq, p = chisquare(couponLengths, expectedValues, 0, None)

    success = ( p >= 0.01)
    return (success,p,None)
