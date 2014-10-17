# Copyright 2013-2014 Lenna X. Peterson. All rights reserved.

import ConfigParser
import errno
import os
import re
import shutil
import StringIO


def read_config(config_path):
    """
    Read in a config file optionally containing whitespace
    (normally fails)
    """
    config = ConfigParser.SafeConfigParser()
    # Strip whitespace from config
    # http://stackoverflow.com/a/12822143
    with open(config_path, "r") as ih:
        config_data = StringIO.StringIO("\n".join(line.strip() for line in ih))
    config.readfp(config_data)
    return config

def copy_file(src, dest):
    if os.path.isfile(dest): return
    shutil.copyfile(src, dest)

def mkdir_p(path):
    """
    Pythonic replacement for shell `mkdir -p`
    Creates multiple directories and ignores error caused by existing
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

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

_h_re = re.compile(r"[123 ]*H.*")

def strip_h(filename):
    """
    Strip hydrogens from PDBfile
    NB loads entire file into memory, use at your own risk
    """
    with open(filename, "r") as ih:
        ret = StringIO.StringIO("\n".join(r for r in ih
                                          if r[:4] != "ATOM"
                                          or not _h_re.match(r[12:16])))
    return ret

def head(iterable, n=10):
    """
    Print first n items of iterable
    """
    for i, v in enumerate(iterable):
        print v
        if i > n:
            break

def range_overlap(range1, range2):
    """
    Return True if ranges have any overlap, else False
    Return None if ranges are not sorted
    """
    x1, x2 = range1
    y1, y2 = range2
    if x2 < x1 or y2 < y1:
        return None
    return x1 < y2 and y1 < x2

def dict_slice(the_dict, desired_keys):
    """
    Pop and return a dict of the named keys from the dict
    NB original dict is modified in place
    the_dict: dict to slice
    desired_keys: keys to return
    """
    return {key: the_dict.pop(key) for key in desired_keys}

def split_index(s, i):
    """Split a string `s` at the specified index `i`"""
    return s[:i], s[i:]

greek_cardinals = dict(
    mono=1, di=2, tri=3, tetra=4, penta=5,
    hexa=6, hepta=7, octa=8, nona=9, deca=10,
    dodeca=12,
)

def parse_mer(mer, suffix="meric"):
    """
    Convert Greek cardinal description of protein complex to integer
    e.g. MONOMERIC -> 1
    DIMERIC -> 2
    """
    mer = mer.strip().lower()
    suf_len = len(suffix)
    if mer[-suf_len:] == suffix:
        root = mer[:-suf_len]
    else:
        raise ValueError("must end in '%s'", suffix)
    number = greek_cardinals.get(root)
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
        raise ValueError("unable to parse '%s'", mer)
