import h5py
import sys
import numpy as np


def data_load(hdfpath, object_id):
    with h5py.File(hdfpath, 'r') as f:
        data = []
        data.append(f[object_id[0]].value)
        # Todo 抽象化
        dimension = f['data/scaleUnit']['dimension'].astype(np.str)
        object_def = f['data/objectDef']['oID']
        f.close()
    return data, dimensional_judge(dimension[0]), object_def


def dimensional_judge(dimension):
    if '3D' in dimension:
        return '3D'
    elif '2D' in dimension:
        return '2D'
    else:
        sys.exit("didn't know the dimensions.")
