"""Unit tests for csv_to_dict_list module."""

import pytest
import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe


@pytest.fixture
def csv_directory(tmp_path):
    """Create a temporary directory with 2 CSV files."""
    csv1 = tmp_path / "users.csv"
    csv1.write_text("name,age\nAlice,30\nBob,25\n")

    csv2 = tmp_path / "more_users.csv"
    csv2.write_text("name,age\nCarol,28\nDave,35\n")

    return tmp_path


def test_read_csvs_to_dataframe_combines_all_rows(csv_directory):
    """Test that all rows from 2 CSV files are combined into one DataFrame."""
    result = read_csvs_to_dataframe(str(csv_directory))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 4
    assert list(result.columns) == ["name", "age"]
    assert "Alice" in result["name"].values
    assert "Bob" in result["name"].values
    assert "Carol" in result["name"].values
    assert "Dave" in result["name"].values
