#!/usr/bin/env python

import sys

import h5py
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import rdMolDescriptors as rdmd
from tqdm import tqdm
from functools import wraps
from time import time
import os.path
import os



def timing(f):
    """
    Decorator to measure execution time, adapted from
    # https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
    # https://codereview.stackexchange.com/questions/169870/decorator-to-measure-execution-time-of-a-function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print(f.__name__, f"Elapsed time: {end - start:.2f} sec")
        return result

    return wrapper


@timing
def make_np_array(lst, dtype=np.float32):
    """
    Convert a list to a numpy array
    :param lst: input list
    :param dtype: data type
    :return: output array
    """
    return np.array(lst, dtype=dtype)

counter=0
@timing
def save_data(fp_array, smiles_list, name_list, outfile_name):
    """
    Write the fingerprints to an hdf5 file
    :param fp_array: numpy array with fingerprints
    :param smiles_list: list of SMILES
    :param name_list: list of molecule names
    :param outfile_name: output file name
    :return: None
    """
    file_exists = os.path.exists(outfile_name)
    h5f = h5py.File(outfile_name, 'a')
    #dt = h5py.special_dtype(vlen=bytes)
    print(fp_array.shape)
    smiles_list=np.array(smiles_list).reshape(-1,1)
    name_list=np.array(name_list).reshape(-1,1)
    print(smiles_list.shape)
    print(name_list.shape)
    global counter
    if(counter==0):
        
    
        fp=h5f.create_dataset('fp_list', data=fp_array,compression="gzip", chunks=True, maxshape=(None,1024))
        print("sahi hai",fp.shape)
        sm=h5f.create_dataset('smiles_list', data=smiles_list,compression="gzip", chunks=True, maxshape=(None,1))
        print(sm.shape)
        nm=h5f.create_dataset('name_list',data=name_list, compression="gzip", chunks=True, maxshape=(None,1) )
        print(nm.shape)
        counter=counter+1
    else:
        h5f['fp_list'].resize((h5f['fp_list'].shape[0] + fp_array.shape[0]), axis=0)
        h5f['fp_list'][-fp_array.shape[0]:] = fp_array

        h5f['smiles_list'].resize((h5f['smiles_list'].shape[0] + smiles_list.shape[0]), axis=0)
        h5f['smiles_list'][-smiles_list.shape[0]:] = smiles_list

        h5f['name_list'].resize((h5f['name_list'].shape[0] + name_list.shape[0]), axis=0)
        h5f['name_list'][-name_list.shape[0]:] = name_list

    h5f.close()


@timing
def generate_fingerprints(infile_name):
    """
    Generate fingerprints from an input file, currently generates a 256 bit morgan fingerprint
    :param infile_name: input file name
    :return: lists with fingerprints, SMILES, and molecule names
    """
    ifs = open(infile_name)
    fp_list = []
    smiles_list = []
    name_list = []
    for line in tqdm(ifs):
        toks = line.strip().split(" ", 1)
        if len(toks) >= 2:
            smiles, name = toks
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                fp = rdmd.GetMorganFingerprintAsBitVect(mol, 2, 1024)
                arr = np.zeros((1,))
                DataStructs.ConvertToNumpyArray(fp, arr)
                fp_list.append(arr)
                smiles_list.append(smiles.encode("ascii", "ignore"))
                name_list.append(name.encode("ascii", "ignore"))
    return fp_list, smiles_list, name_list


@timing
def main(input_smiles_folder, output_fp_file):
    """
    Generate fingerprints and write to an hdf5 file
    :return:
    """
    path=input_smiles_folder
    os.chdir(path)
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".smi"):
            file_path = f"{path}/{file}"
            print(file_path)
            fp_list, smiles_list, name_list = generate_fingerprints(file_path)
            outfile_name = output_fp_file
            fp_array = make_np_array(fp_list)
            print(fp_array.shape)
            save_data(fp_array, smiles_list, name_list, outfile_name)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} infile.smi outfile.h5")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
