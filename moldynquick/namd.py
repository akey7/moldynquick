"""
This module extracts data from NAMD formatted files.

See the following for useful things like units of measurements:

https://www.ks.uiuc.edu/Research/namd/2.9/ug/node12.html
"""

from typing import List, Dict, Any
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import align, rms
import numpy as np


class NAMDLog:
    """
    This class extracts data from a NAMD log file.
    """

    def __init__(self, log_filename: str, fs_per_timestep: int = 2):
        """
        This creates the instance attributes needed to parse the log file.

        Parameters
        ----------
        log_filename: str
            The name of the logfile to extract.

        fs_per_frame: int
            The number of femtoseconds in a frame.
        """
        self.log_filename = log_filename
        self.fs_per_timestep = fs_per_timestep

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
                        "time [fs]": timestep * self.fs_per_timestep,
                        "bond [kcal/mol]": float(values[1]),
                        "angle [kcal/mol]": float(values[2]),
                        "dihedral [kcal/mol]": float(values[3]),
                        "improper [kcal/mol]": float(values[4]),
                        "electrostatic [kcal/mol]": float(values[5]),
                        "VDW [kcal/mol]": float(values[6]),
                        "boundary [kcal/mol]": float(values[7]),
                        "misc [kcal/mol]": float(values[8]),
                        "kinetic [kcal/mol]": float(values[9]),
                        "total [kcal/mol]": float(values[10]),
                        "potential [kcal/mol]": float(values[12]),
                        "total3 [kcal/mol]": float(values[13])
                    }

                    wide.append(wide_row)

        df: pd.DataFrame = pd.DataFrame(wide)
        return df

    def extract_energies_tall(self) -> pd.DataFrame:
        """
        Extracts the narrow format of the schema to a Pandas dataframe.

        Yes this does cause the log file to be read twice. But fixing that
        will need to wait until another version.

        Returns
        -------
        pd.DataFrame
            The dataframe that contains the rows in tall format.
        """
        tall: List[Dict[str, Any]] = []
        wide: pd.DataFrame = self.extract_energies_wide()

        for _, wide_row in wide.iterrows():
            timestep: int = wide_row["timestep"]
            for key, value in wide_row.items():
                if key != "timestep":
                    tall_row = {
                        "timestep": timestep,
                        "measurement": key,
                        "value": value
                    }
                    tall.append(tall_row)

        df: pd.DataFrame = pd.DataFrame(tall)
        return df

    def extract_temperatures(self) -> pd.DataFrame:
        """
        Extracts the temperatures

        Returns
        -------
        pd.DataFrame
            The temperatures.
        """
        rows: List[Dict[str, Any]] = []

        with open(self.log_filename, "r") as file:
            for line in file.readlines():
                if line.startswith("ENERGY:"):
                    values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]
                    timestep = int(values[0])
                    row = {
                        "timestep": timestep,
                        "time [fs]": timestep * self.fs_per_timestep,
                        "temp [K]": float(values[11]),
                        "tempavg [K]": float(values[14])
                    }
                    rows.append(row)

        df = pd.DataFrame(rows)
        return df

    def extract_pressures(self):
        """
        Extracts the pressures

        Returns
        -------
        pd.DataFrame
            The pressures.
        """
        rows: List[Dict[str, Any]] = []

        with open(self.log_filename, "r") as file:
            for line in file.readlines():
                if line.startswith("ENERGY:"):
                    values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]
                    timestep = int(values[0])
                    row = {
                        "timestep": timestep,
                        "time [fs]": timestep * self.fs_per_timestep,
                        "pressure [bar]": float(values[15]),
                        "gpressure [bar]": float(values[16]),
                        "volume [A^3]": float(values[17]),
                        "pressavg [bar]": float(values[18]),
                        "gpressavg [bar]": float(values[19])
                    }
                    rows.append(row)

        df = pd.DataFrame(rows)
        return df


class NAMDTrajectory:
    """
    This extracts trajectory information from the .dcd log file.
    """

    def __init__(self, psf_filename: str, dcd_filename: str, fs_per_frame: int = 2):
        """
        Instantiates with the right filenames to extract trajectory information

        Parameters
        ----------
        psf_filename: str
            The filename to the PSF file.

        dcd_filename: str
            The trajectory DCD file.

        fs_per_frame: int
            The femtoseconds per frame.
        """
        self.psf_filename = psf_filename
        self.dcd_filename = dcd_filename
        self.fs_per_frame = fs_per_frame

    def rmsd_from_first_frame(self, selected_atoms: str = "(protein) and name C CA N") -> pd.DataFrame:
        """
        This calculates the RMSD for every frame from the first frame.

        Parameters
        ----------
        selected_atoms: str
            The selection string to use for the atoms being aligned in
            the trajectory.

        Returns
        -------
        pd.DataFrame
            Dataframe with the columns of frame and RMSD [Å]
        """
        mobile = mda.Universe(self.psf_filename, self.dcd_filename)
        ref = mda.Universe(self.psf_filename, self.dcd_filename)

        # These two lines appear to have no effect, but in reality
        # they set the positions in the trajectory.

        mobile.trajectory[-1]
        ref.trajectory[0]

        aligner = align.AlignTraj(mobile, ref, select=selected_atoms, in_memory=True).run()

        df = pd.DataFrame(data={
            "frame": np.arange(len(aligner.rmsd)),
            "time [fs]": np.arange(len(aligner.rmsd)) * self.fs_per_frame,
            "RMSD [Å]": aligner.rmsd})
        return df
