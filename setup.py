#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='bdmleditor',
    version='1.0',
    description='Editor for hdf5',
    author='Kazuma Inagaki',
    url='https://github.com/tohsato-lab/bdmleditor',
    packages=find_packages(),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'bdmleditor = bdmleditor:main',
        ],
    },
)
