# Copyright 2013-2014 Lenna X. Peterson. All rights reserved.

import glob
import os
import re


class MissingPDBCode(ValueError):
    """Exception for missing PDB code"""


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

    @classmethod
    def pdb_glob(cls, pdb_dir, pdbtype="raw"):
        """Store all valid PDB paths in a dict keyed by PDB code"""
        code_to_path = dict()
        for file_path in glob.iglob(os.path.join(pdb_dir, "*")):
            try:
                code = cls.get_code(os.path.basename(file_path), pdbtype)
            except MissingPDBCode:
                continue
            else:
                code_to_path[code.upper()] = file_path
        return code_to_path

    @classmethod
    def get_code(cls, pdb_string, pdbtype="raw"):
        """
        Retrieve code from PDB string
        pdbtype: name of regexp (raw, mod, unit)
        """
        try:
            regexp = getattr(cls, pdbtype)
        except AttributeError:
            raise ValueError("Unknown pdbtype '%s'", pdbtype)
        else:
            m = regexp.match(pdb_string)
            if not m:
                raise MissingPDBCode(pdb_string)
            else:
                return m.group(1).upper()


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
            try:
                code = pdbre.get_code(pdb_string, testname)
            except MissingPDBCode:
                assert result == 0
            else:
                assert code == "1MBN", code
