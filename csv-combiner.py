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

# empty dataframe
list_of_frames = []
for arg in sys.argv[1:]:
    # dataframe
    df = pd.read_csv(arg)
    # basename column
    df["filename"] = os.path.basename(arg)
    # add dataframe to list
    list_of_frames.append(df)

# concat all dataframes
result = pd.concat(list_of_frames, sort=False)
# convert to csv
result.to_csv(sys.stdout, index=False)
