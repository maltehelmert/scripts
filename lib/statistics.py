# -*- coding: utf-8 -*-

def mean(seq):
    seq = tuple(seq)
    if not seq:
        raise ValueError
    return sum(seq) / float(len(seq))

def variance(seq):
    seq = tuple(seq)
    mu = mean(seq)
    return mean((val - mu) ** 2 for val in seq)

def stddev(seq):
    return variance(seq) ** 0.5

def median(seq):
    seq = sorted(seq)
    if not seq:
        raise ValueError
    if len(seq) % 2 == 1:
        return seq[len(seq) // 2]
    else:
        return 0.5 * (seq[(len(seq) - 1) // 2] + seq[len(seq) // 2])
