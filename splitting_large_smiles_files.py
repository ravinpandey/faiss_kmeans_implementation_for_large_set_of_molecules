# for splitting very smiles files into multiple small files
from itertools import zip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

n = 1500000
import os
with open('Enamine_diversity21m.smi') as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        with open(os.path.join("Data",'small_file_{0}.smi'.format(i * n)), 'w') as fout:
            fout.writelines(g)