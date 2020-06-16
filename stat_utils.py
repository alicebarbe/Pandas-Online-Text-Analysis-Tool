# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:57:23 2019

@author: dgurevich6
"""

# This can be made much better by using scipy
# (which I will probably use extensively in the future)

from math import sqrt, exp

z0 = 1.96  # 95 percentile of normal distribution

def ratio_conf_bounds(k1, n1, k2, n2):
    """Returns 95% lower/upper confidence bounds on ratio, as well as mean.
    Uses Katz logarithm formula.

    Arguments:
            k1, k2 (ints): numbers of successes.
            n1, n2 (ints): total numbers of trials.
    """
    # continuity corrections
    n1adj = n1+0.5
    n2adj = n2+0.5
    k1adj = k1+0.5
    k2adj = k2+0.5
    p1 = k1adj/n1adj  # proportion 1
    p2 = k2adj/n2adj  # proportion 2
    ratio = p1/p2
    sig = sqrt((1-p1)/p1/n1adj+(1-p2)/p2/n2adj)  # standard deviation
    return ratio*exp(-sig*z0), ratio, ratio*exp(sig*z0)
