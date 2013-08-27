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
