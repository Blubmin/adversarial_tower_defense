from functools import reduce
from math import sqrt

def zscore_array(a):
    mu = reduce(lambda x, y: x + y, a) / len(a)

    std_sum = reduce(lambda x, y: x + y, map(lambda x: (x - mu)**2, a))
    sd = sqrt(std_sum / len(a))
    return ([zscore(v, mu, sd) for v in a], mu, sd)

def zscore(v, mu, sd):
    if sd == 0:
        return 0
    return (v - mu) / sd