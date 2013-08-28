# Copyright 2013 Lenna X. Peterson. All rights reserved.

import re


class pdbre(object):
    # PDB file with or without modifications, PDB code in group 1
    mod = re.compile(r"""
                         .*?                 # prefix (lazy)
                         ([0-9][a-z0-9]{3})  # 1 digit, 3 alphanum (group 1)
                         .*                  # suffix (greedy)
                         \.pdb$""", re.IGNORECASE | re.VERBOSE)

    # PDB file w/ or w/o modifications or biounit suffix, PDB code in group 1
    unit = re.compile(r"""
                         .*?                 # prefix (lazy)
                         ([0-9][a-z0-9]{3})  # 1 digit, 3 alphanum (group 1)
                         .*                  # suffix (greedy)
                         \.pdb[1-9]?$""", re.IGNORECASE | re.VERBOSE)

    # Raw PDB file, PDB code in group 1
    raw = re.compile(r"""([0-9][a-z0-9]{3})\.pdb""", re.IGNORECASE)
