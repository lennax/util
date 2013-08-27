#!/usr/bin/env python

from collections import defaultdict
import csv
import logging

from atom_data import AtomData


with open("chi.csv", "rb") as fh:
    r = csv.reader(fh, delimiter=",", quotechar='"')
    rows = list(r)

all_chi = dict()
current_chi = None
for line in rows:
    if not line[1] and line[0][:3] == "CHI":
        current_chi = line[0].lower()
        all_chi[current_chi] = dict()
    if line[1] and current_chi:
        res = line[0]
        atoms = line[2].upper().split("-")
        all_chi[current_chi][res] = atoms

print "all_chi = dict("
for chi in sorted(all_chi.keys()):
    print "    %s=dict(" % chi
    chi_val = all_chi[chi]
    for res in sorted(chi_val.keys()):
        print "        %s=%s," % (res, chi_val[res])
    print "    ),"
print ")"

all_res = defaultdict(set)

for chi_val in all_chi.itervalues():
    for res, atoms in chi_val.iteritems():
        all_res[res].update(atoms)

for res, atoms in all_res.iteritems():
    expected_list = AtomData.res_atom_list[res]
    for atom in atoms:
        if atom not in expected_list:
            logging.warning("Chi atom mismatch: %s, %s, %s",
                            res, expected_list, atom)

print
print "chi_atoms = dict("
for res in sorted(all_res.keys()):
    atoms = all_res[res]
    print "    %s=%s," % (res, repr(atoms))

print ")"
