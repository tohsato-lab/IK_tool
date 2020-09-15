import h5py
import sys
import numpy as np


def data_load(hdfpath, object_path):
    with h5py.File(hdfpath, 'r') as f:
        object_def = f['data/objectDef']['oID']
        data = [[] * 0 for i in range(len(object_def))]
        for i in range(len(object_def)):
            # 無駄に足されている、初期化が必要？
            object_path_swap = ''
            object_path_swap = object_path + str(i)
            data[i].append(f[object_path_swap].value)
        # Todo 抽象化
        dimension = f['data/scaleUnit']['dimension'].astype(np.str)
        f.close()
    return data, dimensional_judge(dimension[0]), object_def


def dimensional_judge(dimension):
    if '3D' in dimension:
        return '3D'
    elif '2D' in dimension:
        return '2D'
    else:
        sys.exit("didn't know the dimensions.")
