import os
import sys

import pandas as pd

"""
Convert .csv to dataframe
Print to terminal

Terminal execution:
$ python csv-combiner.py ./fixtures/accessories.csv
"""

# dataframe
df = pd.read_csv(sys.argv[1])

# basename column
df["filename"] = os.path.basename(sys.argv[1])

# convert to csv
df = df.to_csv(index=False)

# print(df)
sys.stdout.write(df)
