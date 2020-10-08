# bdmleditor ![reviewdog](https://github.com/tohsato-lab/tool/workflows/reviewdog/badge.svg?branch=master)

This is a editor for `hdf5`'s file

## Installation

```
pip install git+https://github.com/tohsato-lab/bdmleditor
```

## Usage

You can use this command in the following ways.

```
$ bdmleditor HDFFILE
```

And you can see all available options by using --help:

```
usage: bdmleditor [-h] [-v] filename

A tool to edit bdml files

positional arguments:
  filename

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

## Development

We are using Pipenv in this project.\
You can recreate the environment using the following methods.\
[pyenv](https://github.com/pyenv/pyenv) may be required. See the official [pipenv](https://github.com/pypa/pipenv)'s reference for details.

1. `pip install pipenv`

2. `git clone https://github.com/tohsato-lab/bdmleditor && cd bdmleditor`

3. `pipenv sync --dev`

4. `pipenv shell`

5. `pip install -e .`
