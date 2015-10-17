import functools

# To extract sequences
from Bio.Data.SCOPData import protein_letters_3to1
from Bio.SeqUtils import seq1
# To align sequences
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo


class PDBAlignError(RuntimeError):
    "Error for class PDBAlign"
    def __init__(self, message):
        super(PDBAlignError, self).__init__(message)


seq1 = functools.partial(seq1, custom_map=protein_letters_3to1)

def align(seq1, seq2):
    matrix = MatrixInfo.blosum100
    gap_open = -10
    gap_extend = -0.5
    alignments = pairwise2.align.globalds(seq1, seq2, matrix, gap_open, gap_extend)
    return alignments[0]

def struct_to_seq(structure, chains=None):
    if not structure.child_list:
        raise PDBAlignError("No models in %s" % structure)
    model = structure.child_list[0]
    if not model.child_list:
        raise PDBAlignError("No chains in %s" % structure)
    if chains is None:
        chain_list = model.child_list
    else:
        chain_list = [model[ch] for ch in chains]
    atom_seq_dict = dict()
    for ch in chain_list:
        # Don't include all-het chain
        if all(res.get_id()[0].strip() for res in ch.child_list):
            continue
        atom_seq_dict[ch.id] = "".join(seq1(res.resname)
                                       for res in ch.child_list
                                       if res.get_id()[0] == " ")
    return atom_seq_dict
