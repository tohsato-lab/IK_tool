#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'numpy',
    'matplotlib',
    'h5py',
    # 'ansicolor>=0.2.4',
    # 'chardet>=2.3.0',
    # 'setuptools>=36.2.2',  # for enhanced marker support (used below).
    # 'enum34>=1.0.4;python_version<"3.4"',
    # 'pathlib>=1.0.1;python_version<"3.4"',
    # 'typing>=3.6.2;python_version<"3.6"',
]

setup(
    name='bdmleditor',
    version='1.0',
    description='Editor for hdf5',
    author='Kazuma Inagaki',
    url='https://github.com/tohsato-lab/bdmleditor',
    install_requires=install_requires,
    packages=find_packages(),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'bdmleditor = bdmleditor:main',
        ],
    },
)
