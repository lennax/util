# Copyright 2013 Lenna X. Peterson. All rights reserved.

import collections


class ReadPDB(object):

    def __init__(self, pdb_list):
        """Load list of PDBs for iteration"""
        self.load_codes(pdb_list)

    def __iter__(self):
        """Yield pdbcodes and associated chain list"""
        for k, v in self.pdb_dict.iteritems():
            # Replace a list of empty strings with empty list
            if not any(v):
                v = list()
            yield dict(pdbcode=k, chainlist=v)

    def load_codes(self, pdb_list):
        """Load PDB code and chain(s) from space-delimited list"""
        with open(pdb_list, "rb") as fh:
            pisces_list = list(fh)
        pdb_dict = collections.defaultdict(list)
        for i, line in enumerate(pisces_list):
            if i == 0:
                line = self.guess_header(line)
                if line is None:
                    continue
            full_code = line.split()[0]
            if len(full_code) < 4:
                raise ValueError("Invalid PDB code %s", full_code)
            code, chain = self.split_index(full_code, 4)
            pdb_dict[code].append(chain)
        # Convert defaultdict to normal dict
        self.pdb_dict = dict(pdb_dict)

    @staticmethod
    def split_index(s, i):
        """Split a string `s` at the specified index `i`"""
        return s[:i], s[i:]

    @staticmethod
    def guess_header(line, first_col="IDs", val_len="5"):
        """
        Guess whether a `line` is a header based on:
            first_col: expected first column header
            val_len:   expected first value length
        """
        col = line.split()[0]
        if col != first_col or len(col) == val_len:
            return line
