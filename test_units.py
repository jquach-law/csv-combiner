import os
import sys

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from csv_combiner import CSVCombiner

csv_combiner = CSVCombiner()


def test_always_passes():
    assert True


# _validate_zero_argument
def test_validate_zero_argument_01():
    with pytest.raises(
        ValueError, match="Error: Need at least 1 .csv file, 0 is given"
    ):
        csv_combiner.argv = []
        csv_combiner._validate_zero_argument()


def test_validate_zero_argument_02():
    with pytest.raises(
        ValueError, match="Error: Need at least 1 .csv file, 0 is given"
    ):
        csv_combiner.argv = ["be_tested.py"]
        csv_combiner._validate_zero_argument()


def test_validate_zero_argument_03():
    csv_combiner.argv = [
        "be_tested.py",
        "./fixtures/accessories.csv",
        "./fixtures/clothing.csv",
    ]
    assert csv_combiner._validate_zero_argument() is True


# _validate_csv_filename
def test_validate_csv_filename_01():
    with pytest.raises(
        ValueError, match="Error: Expected .csv file, received be_tested.py"
    ):
        csv_combiner.argv = ["be_tested.py", "xyz"]
        csv_combiner._validate_csv_filename()


def test_validate_csv_filename_02():
    csv_combiner.argv = [
        "./fixtures/accessories.csv", "./fixtures/clothing.csv"]
    assert csv_combiner._validate_csv_filename() is True


# _add_filename_column
def test_add_filename_column_01():
    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df2 = csv_combiner._add_filename_column(df1, "temp.csv")
    df1["filename"] = os.path.basename("temp.csv")
    assert_frame_equal(df1, df2)


# _read_csv_to_dataframe
def test_read_csv_to_dataframe_01():
    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df1.to_csv("temp.csv", index=False)
    df2 = csv_combiner._read_csv_to_dataframe("temp.csv")
    df1["filename"] = os.path.basename("temp.csv")
    assert_frame_equal(df1, df2)
    os.remove("temp.csv")


def test_read_csv_to_dataframe_02():
    with pytest.raises(FileNotFoundError):
        csv_combiner._read_csv_to_dataframe("sdfe.csv")


def test_read_csv_to_dataframe_03():
    file_data = "colA,colB,colC,colD\n1,A,100,1.0\n2,B,121,2.1\n3,C,122,10.1,,\n4,D,164,3.1\n5,E,55,4.5\n6,F,121,1.1,,"
    with open("parse_error.txt", "w") as file:
        file.write(file_data)
    with pytest.raises(pd.errors.ParserError):
        csv_combiner._read_csv_to_dataframe("parse_error.txt")
    os.remove("parse_error.txt")


def test_combine_csv_01(capsys):
    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df1.to_csv("temp01.csv", index=False)
    df2 = pd.DataFrame({"a": [5, 6], "z": [None, "hello"], "b": [7, 8]})
    df2.to_csv("temp02.csv", index=False)
    csv_combiner.argv = ["temp01.csv", "temp02.csv"]
    csv_combiner.combine_csv()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "a,b,filename,z\n1,3,temp01.csv,\n2,4,temp01.csv,\n5,7,temp02.csv,\n6,8,temp02.csv,hello\n"
    )
    os.remove('temp01.csv')
    os.remove('temp02.csv')
