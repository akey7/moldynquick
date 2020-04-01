# moldynquick
mol-DYN-quick is a simple tool to run essential analysis after you run a trajectory with NAMD. Skip Tcl and xmgrace. Use moldynquick! (A bad name, I know. But it was late at night and I needed a name for the repo...)

It is a command line tool aimed primarily and macOS and Windows.

## Installation

This guide assumes you are using Anaconda and Python 3.8 from the command line.

First, fork and clone this repo.

### 1. New virtual environment

``` 
conda create -n moldynquick python=3.8
```

and don't forget to activate it:

```
conda activate moldynquick
```

### 2. Install the actual package

From the root of the repo

``` 
pip install -e .
```

### 3. Run it!

See the command line options!

``` 
python -m moldynquick -h
```
