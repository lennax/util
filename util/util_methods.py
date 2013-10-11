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


def dict_slice(the_dict, desired_keys):
    """
    Return a dict of the named keys from the dict
    the_dict: dict to slice
    desired_keys: keys to return
    """
    return {key: the_dict.pop(key) for key in desired_keys}


def split_index(s, i):
    """Split a string `s` at the specified index `i`"""
    return s[:i], s[i:]


latins = dict(
    mono=1, di=2, tri=3, tetra=4, penta=5,
    hexa=6, hepta=7, octa=8, nona=9, deca=10,
    dodeca=12,
)

def parse_mer(mer, suffix="meric"):
    mer = mer.strip().lower()
    suf_len = len(suffix)
    if mer[-suf_len:] == suffix:
        root = mer[:-suf_len]
    else:
        raise ValueError("must end in '%s'", suffix)
    number = latins.get(root)
    if number is not None:
        return number
    else:
        if root.endswith("-"):
            try:
                number = int(root[:-1])
            except ValueError:
                pass
            else:
                return number
        else:
            raise ValueError("unable to parse '%s'", mer)
