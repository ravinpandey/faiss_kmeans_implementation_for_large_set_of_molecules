# for splitting very smiles files into multiple small files
from itertools import zip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

n = 500000
import os

with open('/home/ravindra/ravindra/RAVI_BACKUP/MolecularClustering/Data/Enamine_diversity21m.smi') as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        with open(os.path.join("//home/ravindra/ravindra/RAVI_BACKUP/MolecularClustering/Data/DATA",'Enamine_diversity21m_{0}.smi'.format(i * n)), 'w') as fout:
            fout.writelines(g)