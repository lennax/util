# Copyright 2013-2015 Lenna X. Peterson. All rights reserved.


from .meta import classproperty


class AtomData(object):

    # Maximum ASA for each residue
    # from Miller et al. 1987, JMB 196: 641-656
    total_asa = {
        'A': 113.0,
        'R': 241.0,
        'N': 158.0,
        'D': 151.0,
        'C': 140.0,
        'Q': 189.0,
        'E': 183.0,
        'G': 85.0,
        'H': 194.0,
        'I': 182.0,
        'L': 180.0,
        'K': 211.0,
        'M': 204.0,
        'F': 218.0,
        'P': 143.0,
        'S': 122.0,
        'T': 146.0,
        'W': 259.0,
        'Y': 229.0,
        'V': 160.0,
    }

    @classmethod
    def is_surface(cls, resn, asa, total_asa=None, cutoff=0.1):
        """Return True if ratio of residue ASA to max ASA >= cutoff"""
        if total_asa is None:
            total_asa = cls.total_asa
        resn = resn.upper()
        if len(resn) == 3:
            resn = cls.three_to_one[resn]
        return float(asa) / total_asa[resn] >= cutoff

    three_to_full = {
        'Val': 'Valine', 'Ile': 'Isoleucine', 'Leu': 'Leucine',
        'Glu': 'Glutamic acid', 'Gln': 'Glutamine',
        'Asp': 'Aspartic acid', 'Asn': 'Asparagine', 'His': 'Histidine',
        'Trp': 'Tryptophan', 'Phe': 'Phenylalanine', 'Tyr': 'Tyrosine',
        'Arg': 'Arginine', 'Lys': 'Lysine',
        'Ser': 'Serine', 'Thr': 'Threonine',
        'Met': 'Methionine', 'Ala': 'Alanine',
        'Gly': 'Glycine', 'Pro': 'Proline', 'Cys': 'Cysteine'}

    three_to_one = {
        'VAL': 'V', 'ILE': 'I', 'LEU': 'L', 'GLU': 'E', 'GLN': 'Q',
        'ASP': 'D', 'ASN': 'N', 'HIS': 'H', 'TRP': 'W', 'PHE': 'F', 'TYR': 'Y',
        'ARG': 'R', 'LYS': 'K', 'SER': 'S', 'THR': 'T', 'MET': 'M', 'ALA': 'A',
        'GLY': 'G', 'PRO': 'P', 'CYS': 'C'}

    one_to_three = {o: t for t, o in three_to_one.iteritems()}

    @classproperty
    def one_to_full(cls):
        """
        This can't see three_to_full unless explicitly passed because
        dict comprehensions create their own local scope
        """
        return {o: cls.three_to_full[t.title()] for t, o in cls.three_to_one.iteritems()}

    res_atom_list = dict(
        ALA=['C', 'CA', 'CB', 'N', 'O'],
        ARG=['C', 'CA', 'CB', 'CD', 'CG', 'CZ', 'N', 'NE', 'NH1', 'NH2', 'O'],
        ASN=['C', 'CA', 'CB', 'CG', 'N', 'ND2', 'O', 'OD1'],
        ASP=['C', 'CA', 'CB', 'CG', 'N', 'O', 'OD1', 'OD2'],
        CYS=['C', 'CA', 'CB', 'N', 'O', 'SG'],
        GLN=['C', 'CA', 'CB', 'CD', 'CG', 'N', 'NE2', 'O', 'OE1'],
        GLU=['C', 'CA', 'CB', 'CD', 'CG', 'N', 'O', 'OE1', 'OE2'],
        GLY=['C', 'CA', 'N', 'O'],
        HIS=['C', 'CA', 'CB', 'CD2', 'CE1', 'CG', 'N', 'ND1', 'NE2', 'O'],
        ILE=['C', 'CA', 'CB', 'CD1', 'CG1', 'CG2', 'N', 'O'],
        LEU=['C', 'CA', 'CB', 'CD1', 'CD2', 'CG', 'N', 'O'],
        LYS=['C', 'CA', 'CB', 'CD', 'CE', 'CG', 'N', 'NZ', 'O'],
        MET=['C', 'CA', 'CB', 'CE', 'CG', 'N', 'O', 'SD'],
        PHE=['C', 'CA', 'CB', 'CD1', 'CD2',
                        'CE1', 'CE2', 'CG', 'CZ', 'N', 'O'],
        PRO=['C', 'CA', 'CB', 'CD', 'CG', 'N', 'O'],
        SER=['C', 'CA', 'CB', 'N', 'O', 'OG'],
        THR=['C', 'CA', 'CB', 'CG2', 'N', 'O', 'OG1'],
        TRP=['C', 'CA', 'CB', 'CD1', 'CD2', 'CE2',
                        'CE3', 'CG', 'CH2', 'CZ2', 'CZ3', 'N', 'NE1', 'O'],
        TYR=['C', 'CA', 'CB', 'CD1', 'CD2',
                        'CE1', 'CE2', 'CG', 'CZ', 'N', 'O', 'OH'],
        VAL=['C', 'CA', 'CB', 'CG1', 'CG2', 'N', 'O'],
    )

    all_chi = dict(
        chi1=dict(
            ARG=['N', 'CA', 'CB', 'CG'],
            ASN=['N', 'CA', 'CB', 'CG'],
            ASP=['N', 'CA', 'CB', 'CG'],
            CYS=['N', 'CA', 'CB', 'SG'],
            GLN=['N', 'CA', 'CB', 'CG'],
            GLU=['N', 'CA', 'CB', 'CG'],
            HIS=['N', 'CA', 'CB', 'CG'],
            ILE=['N', 'CA', 'CB', 'CG1'],
            LEU=['N', 'CA', 'CB', 'CG'],
            LYS=['N', 'CA', 'CB', 'CG'],
            MET=['N', 'CA', 'CB', 'CG'],
            PHE=['N', 'CA', 'CB', 'CG'],
            PRO=['N', 'CA', 'CB', 'CG'],
            SER=['N', 'CA', 'CB', 'OG'],
            THR=['N', 'CA', 'CB', 'OG1'],
            TRP=['N', 'CA', 'CB', 'CG'],
            TYR=['N', 'CA', 'CB', 'CG'],
            VAL=['N', 'CA', 'CB', 'CG1'],
        ),
        chi2=dict(
            ARG=['CA', 'CB', 'CG', 'CD'],
            ASN=['CA', 'CB', 'CG', 'OD1'],
            ASP=['CA', 'CB', 'CG', 'OD1'],
            GLN=['CA', 'CB', 'CG', 'CD'],
            GLU=['CA', 'CB', 'CG', 'CD'],
            HIS=['CA', 'CB', 'CG', 'ND1'],
            ILE=['CA', 'CB', 'CG1', 'CD1'],
            LEU=['CA', 'CB', 'CG', 'CD1'],
            LYS=['CA', 'CB', 'CG', 'CD'],
            MET=['CA', 'CB', 'CG', 'SD'],
            PHE=['CA', 'CB', 'CG', 'CD1'],
            PRO=['CA', 'CB', 'CG', 'CD'],
            TRP=['CA', 'CB', 'CG', 'CD1'],
            TYR=['CA', 'CB', 'CG', 'CD1'],
        ),
        chi3=dict(
            ARG=['CB', 'CG', 'CD', 'NE'],
            GLN=['CB', 'CG', 'CD', 'OE1'],
            GLU=['CB', 'CG', 'CD', 'OE1'],
            LYS=['CB', 'CG', 'CD', 'CE'],
            MET=['CB', 'CG', 'SD', 'CE'],
        ),
        chi4=dict(
            ARG=['CG', 'CD', 'NE', 'CZ'],
            LYS=['CG', 'CD', 'CE', 'NZ'],
        ),
        chi5=dict(
            ARG=['CD', 'NE', 'CZ', 'NH1'],
        ),
    )

    alt_chi = dict(
        chi1=dict(
            VAL=['N', 'CA', 'CB', 'CG2'],
        ),
        chi2=dict(
            ASP=['CA', 'CB', 'CG', 'OD2'],
            LEU=['CA', 'CB', 'CG', 'CD2'],
            PHE=['CA', 'CB', 'CG', 'CD2'],
            TYR=['CA', 'CB', 'CG', 'CD2'],
        ),
    )

    chi_atoms = dict(
        ARG=set(['CB', 'CA', 'CG', 'NE', 'N', 'CZ', 'NH1', 'CD']),
        ASN=set(['CB', 'CA', 'N', 'CG', 'OD1']),
        ASP=set(['CB', 'CA', 'N', 'CG', 'OD1', 'OD2']),
        CYS=set(['CB', 'CA', 'SG', 'N']),
        GLN=set(['CB', 'CA', 'CG', 'N', 'CD', 'OE1']),
        GLU=set(['CB', 'CA', 'CG', 'N', 'CD', 'OE1']),
        HIS=set(['ND1', 'CB', 'CA', 'CG', 'N']),
        ILE=set(['CG1', 'CB', 'CA', 'CD1', 'N']),
        LEU=set(['CB', 'CA', 'CG', 'CD1', 'CD2', 'N']),
        LYS=set(['CB', 'CA', 'CG', 'CE', 'N', 'NZ', 'CD']),
        MET=set(['CB', 'CA', 'CG', 'CE', 'N', 'SD']),
        PHE=set(['CB', 'CA', 'CG', 'CD1', 'CD2', 'N']),
        PRO=set(['CB', 'CA', 'N', 'CG', 'CD']),
        SER=set(['OG', 'CB', 'CA', 'N']),
        THR=set(['CB', 'CA', 'OG1', 'N']),
        TRP=set(['CB', 'CA', 'CG', 'CD1', 'N']),
        TYR=set(['CB', 'CA', 'CG', 'CD1', 'CD2', 'N']),
        VAL=set(['CG1', 'CG2', 'CB', 'CA', 'N']),
    )
