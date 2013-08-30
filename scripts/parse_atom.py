#!/usr/bin/env python
# Copyright 2013 Lenna X. Peterson. All rights reserved.

from collections import defaultdict
import logging
import re


from atom_data import AtomData


h_re = re.compile(r"""^\d?H""")

atoms = defaultdict(list)
with open("atom_nom.csv", "rb") as fh:
    for line in fh:
        line = line.strip()
        if line:
            line = line.split()
            if len(line) != 2:
                logging.warning(line)
            else:
                residue, atom = line
            res_three = AtomData.one_to_three.get(residue)
            if h_re.match(atom) or not res_three:
                logging.warning("Skipping hydrogen: %s", atom)
                continue
            atoms[res_three].append(atom)

for val in atoms.itervalues():
    val.sort()
    assert "N" in val
    assert "C" in val
    assert "CA" in val
    assert "O" in val

print "res_atom_list = dict("

for res in sorted(atoms.keys()):
    print "    %s=%s," % (res, atoms[res])

print ")"
