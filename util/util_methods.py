# Copyright 2013 Lenna X. Peterson. All rights reserved.


def venn(left, right):
    """
    Return a 3-tuple of:
        the items unique to the left iterable,
        the shared items,
        the items unique to the right iterable
    """
    left = set(left)
    right = set(right)
    return left - right, left & right, right - left


def head(iterable, n=10):
    for i, v in enumerate(iterable):
        print v
        if i > n:
            break

def range_overlap(range1, range2):
    """
    Return True if ranges have any overlap, else False
    """
    x1, x2 = range1
    y1, y2 = range2
    if x2 < x1 or y2 < y1:
        return None
    return x1 < y2 and y1 < x2
