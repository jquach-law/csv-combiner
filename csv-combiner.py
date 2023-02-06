import os
import sys

import pandas as pd

"""
Convert multiple .csv to dataframe
Print to terminal or redirect with '>'

Terminal execution:
$ python csv-combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv
$ python csv-combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv
"""


def check_file_type():
    if len(sys.argv) == 0:
        pass

    for arg in sys.argv[1:]:
        if not arg.endswith(".csv"):
            print("Error: Expected .csv file", file=sys.stderr)
            sys.exit(1)


def combine_csv():
    # empty list to hold dataframe(s)
    list_of_frames = []

    for arg in sys.argv[1:]:
        # csv to dataframe
        try:
            df = pd.read_csv(arg)
        except FileNotFoundError:
            print(f"Error: File not found: '{arg}'", file=sys.stderr)
            sys.exit(1)
        except pd.errors.ParserError as e:
            print(f"Error: Parsing error: '{arg}'\n", e, file=sys.stderr)
            sys.exit(1)

        # add basename column
        df["filename"] = os.path.basename(arg)
        # add dataframe to list
        list_of_frames.append(df)

    # concatenate all dataframes
    result = pd.concat(list_of_frames, sort=False)
    # convert to csv & output
    result.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    check_file_type()
    combine_csv()
