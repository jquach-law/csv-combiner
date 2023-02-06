import os
import sys

import pandas as pd


class CSVCombiner:
    def __init__(self, arguments=sys.argv[1:]):
        self.argv = arguments

    def _validate_zero_argument(self):
        # Validate at least one argument is given
        if len(self.argv) <= 1:
            raise ValueError(f"Error: Need at least 1 .csv file, 0 is given")
        return True

    def _validate_csv_filename(self):
        # Validate files end with .csv
        for arg in self.argv:
            if not arg.endswith(".csv"):
                raise ValueError(f"Error: Expected .csv file, received {arg}")
        return True

    def _add_filename_column(self, df, file_path):
        # Add 'filename' column to dataframe
        df["filename"] = os.path.basename(file_path)
        return df

    def _read_csv_to_dataframe(self, file_path):
        # Read .csv in chunks
        try:
            chunks = pd.read_csv(file_path, chunksize=10**3)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File not found: '{file_path}'")
        except pd.errors.ParserError:
            raise pd.errors.ParserError(f"Error: Parsing error: '{file_path}'")

        # Concatenate chunks to dataframe
        df = pd.concat(chunks)

        df = self._add_filename_column(df, file_path)
        return df

    def combine_csv(self):
        # Validate user's input arguments
        self._validate_zero_argument()
        self._validate_csv_filename()
        # Create and hold dataframe for each .csv argument
        list_of_frames = [self._read_csv_to_dataframe(arg) for arg in self.argv]
        # Concatenate all dataframes
        result = pd.concat(list_of_frames, sort=False)
        # Convert dataframe to csv & output
        result.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    csv_combiner = CSVCombiner()
    # Try-Block to catch raised exceptions
    try:
        csv_combiner.combine_csv()
    except (FileNotFoundError, pd.errors.ParserError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
