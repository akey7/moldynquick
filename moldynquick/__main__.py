from time import time
from argparse import ArgumentParser
import pandas as pd

from moldynquick.namd import NAMDLog


class App:
    def __init__(self):
        """
        This initializes the instance attributes that will hold filenames for
        input and output, as well as the timestamp
        """
        self.timestamp = str(round(time()))
        self.log_filename = None
        self.psf_filename = None
        self.dcd_filename = None
        self.filename_title = None

    @property
    def timestampped_title(self) -> str:
        """
        Concatenates the title and the timestamp together.

        Returns
        -------
        str
            The timestamped title
        """
        return f"{self.filename_title}.{self.timestamp}"

    def parse_the_arguments(self) -> None:
        """
        This parses the command line arguments into the instance attributes
        """
        parser: ArgumentParser = ArgumentParser()

        parser.add_argument("--log", "-l",
                            help="The logfile as captured from stdout when NAMD is executed.",
                            type=str)

        parser.add_argument("--dcd", "-d",
                            help="The .dcd format trajectory file.",
                            type=str)

        parser.add_argument("--psf", "-p",
                            help="Protein structure file in .psf format.",
                            type=str)

        parser.add_argument("--title", "-t",
                            help="The title for the output files. This will be used with the timestamp to create filenames.",
                            type=str)

        args = parser.parse_args()

        self.log_filename = args.log if args.log is not None else "default.log"
        self.dcd_filename = args.dcd if args.dcd is not None else "default.dcd"
        self.psf_filename = args.psf if args.psf is not None else "default.psf"
        self.filename_title = args.title if args.title is not None else "default"

    def create_xlsx(self) -> None:
        """
        Creates the Excel file.
        """
        xlsx_filename: str = f"{self.timestampped_title}.xlsx"

        namd_log: NAMDLog = NAMDLog(self.log_filename)

        print("EXTRACT: Energies from NAMD log file.")
        energies_wide = namd_log.extract_energies_wide()
        energies_tall = namd_log.extract_energies_tall()


        print(f"WRITE: Creating {xlsx_filename}")
        with pd.ExcelWriter(xlsx_filename) as writer:
            energies_wide.to_excel(writer, "Energies wide", index=False)
            energies_tall.to_excel(writer, "Energies tall", index=False)

    def run(self) -> None:
        """
        This runs the app after presenting the user with the input and output
        titles.
        """
        self.parse_the_arguments()
        print(f"Title: {self.timestampped_title}")
        print(f"PSF: {self.psf_filename}")
        print(f"DCD: {self.dcd_filename}")
        print(f"LOG: {self.log_filename}")

        self.create_xlsx()

        print("DONE")


if __name__ == "__main__":
    app = App()
    app.run()
