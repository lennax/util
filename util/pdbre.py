# Copyright 2013 Lenna X. Peterson. All rights reserved.

import re


class pdbre(object):

    # Raw PDB file, PDB code in group 1
    raw = re.compile(r"""(\d[a-z\d]{3})\.pdb$""", re.IGNORECASE)

    # PDB file with or without modifications, PDB code in group 1
    mod = re.compile(r"""
                         . *?            # prefix (lazy)
                         (\d[a-z\d]{3})  # 1 digit, 3 alphanum (group 1)
                         . *             # suffix (greedy)
                         \.pdb$          # file extension, EOL
                     """, re.IGNORECASE | re.VERBOSE)

    # PDB file w/ or w/o modifications or biounit suffix, PDB code in group 1
    unit = re.compile(r"""
                         . *?            # prefix (lazy)
                         (\d[a-z\d]{3})  # 1 digit, 3 alphanum (group 1)
                         . *             # suffix (greedy)
                         \.pdb           # file extension
                         [1-9] ? $       # optional digit, EOL
                      """, re.IGNORECASE | re.VERBOSE)

if __name__ == "__main__":

    test_data = {
        '1mbn.pdb':       {'raw': 1, 'mod': 1, 'unit': 1},
        'prefix1mbn.pdb': {'raw': 0, 'mod': 1, 'unit': 1},
        '1mbnsuffix.pdb': {'raw': 0, 'mod': 1, 'unit': 1},
        '1mbn_0001.pdb':  {'raw': 0, 'mod': 1, 'unit': 1},
        '1mbn.pdb1':      {'raw': 0, 'mod': 0, 'unit': 1},
    }

    for pdb_string, result_dict in test_data.iteritems():
        for testname, result in result_dict.iteritems():
            pattern = getattr(pdbre, testname)
            match = pattern.match(pdb_string)
            assert bool(match) == bool(result)
            if match:
                assert match.group(1) == "1mbn"
