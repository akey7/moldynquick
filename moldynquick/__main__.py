from argparse import ArgumentParser


class App:
    def __init__(self):
        self.log_filename = None
        self.psf_filename = None
        self.dcd_filename = None

    def parse_the_arguments(self) -> None:
        parser: ArgumentParser = ArgumentParser()

        parser.add_argument("--log", "-l",
                            help="The logfile as captured from stdout when NAMD is executed.",
                            type=str)

        parser.add_argument("--dcd", "-d",
                            help="The .dcd format trajectory file",
                            type=str)

        parser.add_argument("--psf", "-p",
                            help="Protein structure file",
                            type=str)

        args = parser.parse_args()

        self.log_filename = args.log if args.log is not None else "default.log"
        self.dcd_filename = args.dcd if args.dcd is not None else "default.dcd"
        self.psf_filename = args.psf if args.psf is not None else "default.psf"

    def run(self) -> None:
        self.parse_the_arguments()
        print(f"PSF: {self.psf_filename}")
        print(f"DCD: {self.dcd_filename}")
        print(f"LOG: {self.log_filename}")


if __name__ == "__main__":
    app = App()
    app.run()
