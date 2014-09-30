# Copyright 2013 Lenna X. Peterson. All rights reserved.

import collections
import os


class ReadPDB(object):

    method_sep = "-"
    ext = ".pdb"

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
        try:
            with open(pdb_list, "rb") as fh:
                pisces_list = list(fh)
        except TypeError:
            pisces_list = pdb_list
        pdb_dict = collections.defaultdict(list)
        for i, line in enumerate(pisces_list):
            if i == 0:
                line = self.guess_header(line)
                if line is None:
                    continue
            line = line.split()
            full_code = line[0]
            if len(full_code) < 4:
                raise ValueError("Invalid PDB code %s", full_code)
            code, chain = self.split_index(full_code, 4)
            if not chain:
                if len(line[1]) == 1 and line[1].isalpha():
                    chain = line[1]
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

    @classmethod
    def make_method_key(cls, code, grp, method):
        """Combine PDB code, PDB group, and method"""
        # Force join to raise an error if code is missing
        if not code:
            code = None
        else:
            code = code.encode().upper()
        if grp is None:
            grp = ""
        else:
            grp = grp.encode()
        if method is None:
            method = "raw"
        else:
            method = method.encode()
        return cls.method_sep.join((code, grp, method))

    @classmethod
    def split_method_code(cls, method_key):
        """Extract PDB code from method key"""
        return method_key.split(cls.method_sep)[0]

    @classmethod
    def get_method_raw(cls, method_key):
        """Remove method (last item) from method key"""
        return cls.method_sep.join(method_key.split(cls.method_sep)[:-1])

    @classmethod
    def split_method(cls, method_key):
        """Extract method from method key"""
        return method_key.split(cls.method_sep)[-1]

    @classmethod
    def make_pdbfile(cls, pdbcode, pdb_base, method=None):
        if method:
            pdbcode = cls.make_method_key(code=pdbcode, method=method)
        return os.path.join(pdb_base, pdbcode + cls.ext)
