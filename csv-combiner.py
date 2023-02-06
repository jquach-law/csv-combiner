import os
import sys

import pandas as pd


def validate_input_files():
    """
    DOCSTRING
    """
    # Validate at least one argument is given
    if len(sys.argv) <= 1:
        raise ValueError(f"Error: Need at least 1 .csv file, 0 is given")

    # Validate files end with .csv
    for arg in sys.argv[1:]:
        if not arg.endswith(".csv"):
            raise ValueError(f"Error: Expected .csv file, received {arg}")


def read_csv(file_path):
    """
    DOCSTRING
    """
    # Read .csv to dataframe
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found: '{file_path}'")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error: Parsing error: '{file_path}'")

    # Add 'filename' column to dataframe
    df["filename"] = os.path.basename(file_path)

    return df


def combine_csv():
    """
    DOCSTRING
    """
    # Create and hold dataframe for each .csv argument
    list_of_frames = [read_csv(arg) for arg in sys.argv[1:]]
    # Concatenate all dataframes
    result = pd.concat(list_of_frames, sort=False)
    # Convert to csv & output
    result.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    # Try-Block to catch raised exceptions
    try:
        validate_input_files()
        combine_csv()
    except (FileNotFoundError, pd.errors.ParserError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
