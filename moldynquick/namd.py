"""
This module extracts data from NAMD formatted files
"""

from typing import List, Dict, Any
import pandas as pd


class NAMDLog:
    """
    This class extracts data from a NAMD log file.
    """

    def __init__(self, log_filename: str):
        """
        This creates the instance attributes needed to parse the log file.

        Parameters
        ----------
        log_filename: str
            The name of the logfile to extract.
        """
        self.log_filename = log_filename

    def extract_energies_wide(self) -> pd.DataFrame:
        """
        This extracts the energies from the log file and returns a dataframe
        that has those energies in it.

        Returns
        -------
        pd.DataFrame
            A dataframe of the energies in wid (pivoted) format.
        """
        wide: List[Dict[str, Any]] = []

        with open(self.log_filename, "r") as file:
            for line in file.readlines():
                if line.startswith("ENERGY:"):
                    values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]

                    timestep = int(values[0])

                    wide_row = {
                        "timestep": timestep,
                        "bond [kcal/mol]": float(values[1]),
                        "angle [kcal/mol]": float(values[2]),
                        "dihedral [kcal/mol]": float(values[3]),
                        "improper [kcal/mol]": float(values[4]),
                        "electrostatic [kcal/mol]": float(values[5]),
                        "VDW [kcal/mol]": float(values[6]),
                        "temp [K]": float(values[11])
                    }

                    wide.append(wide_row)

        df: pd.DataFrame = pd.DataFrame(wide)
        return df
