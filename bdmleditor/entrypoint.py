import argparse
import platform
from bdmleditor.bootstrap import data_load
from bdmleditor.bootstrap import objectdef_load
import os
import sys


def _get_version():
    __version__ = '1.0.0'
    return ('%s Python %s on %s' %
            (__version__, platform.python_version(), platform.system()))


# entry point
def arg_check():
    parser = argparse.ArgumentParser(prog='bdmleditor', description='A tool to edit bdml files')
    parser.add_argument('filename')
    parser.add_argument('-v', '--version', action='version', version=_get_version())
    args = parser.parse_args()
    return args


def list_parse(data_time, object_def, hdfpath):
    if object_def in objectdef_load(hdfpath):
        return ['data/', str(data_time), '/object/', str(object_def)]
    else:
        sys.exit("no exists objectdef")


def entry_point(args):
    check_extension(args)
    print('objectdef list: {0}'.format(objectdef_load(args.filename)))
    # Todo 抽象性をあげよう...
    data = list_parse(int(input('Enter time:')),
                      int(input('Enter objectdef:')),
                      args.filename)
    info = data_load(args.filename, ''.join(data))
    if info[1] == '2D':
        from bdmleditor.plotter.plot_2d import Plot_2D
        bdml_object = Plot_2D(info[0][0], args.filename, data)
        bdml_object.run()
    elif info[1] == '3D':
        from bdmleditor.plotter.plot_3d import Plot_3D
        bdml_object = Plot_3D(info[0][0], args.filename, data)
        bdml_object.run()


def check_extension(args):
    filename, ext = os.path.splitext(args.filename)
    if ext != '.h5':
        sys.exit('This is not .h5 file')
