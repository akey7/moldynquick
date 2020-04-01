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

## Citations

This work incorporate [MDAnalysis](http://mdanalysis.org), a fantastic package to analyze MD trajectories in Python. These are the citations that make MDAnalysis possible:

N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein. MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations. J. Comput. Chem. 32 (2011), 2319–2327. [doi:10.1002/jcc.21787](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.21787)

R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler, D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein. [MDAnalysis: A Python package for the rapid analysis of molecular dynamics simulations.](http://conference.scipy.org/proceedings/scipy2016/oliver_beckstein.html) In S. Benthall and S. Rostrup, editors, Proceedings of the 15th Python in Science Conference, pages 98-105, Austin, TX, 2016. SciPy. [doi:10.25080/Majora-629e541a-00e](https://conference.scipy.org/proceedings/scipy2016/oliver_beckstein.html)

Douglas L. Theobald. Rapid calculation of RMSD using a quaternion-based characteristic polynomial. Acta Crystallographica A 61 (2005), 478-480.

Pu Liu, Dmitris K. Agrafiotis, and Douglas L. Theobald. Fast determination of the optimal rotational matrix for macromolecular superpositions. J. Comput. Chem. 31 (2010), 1561–1563.

For more details on the citations, please see the [MDAnalysis Quick Start Guide References Section.](https://www.mdanalysis.org/UserGuide/examples/quickstart.html#References)
