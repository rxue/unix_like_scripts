"""Unit tests for csv_to_dict module."""

import pytest
from pathlib import Path

from csv_to_dict import read_csvs_to_dict


@pytest.fixture
def csv_directory(tmp_path):
    """Create a temporary directory with sample CSV files."""
    # Create first CSV file
    csv1 = tmp_path / "users.csv"
    csv1.write_text("name,age\nAlice,30\nBob,25\n")

    # Create second CSV file
    csv2 = tmp_path / "products.csv"
    csv2.write_text("id,name,price\n1,Apple,1.50\n2,Banana,0.75\n")

    return tmp_path


def test_read_csvs_to_dict_returns_correct_structure(csv_directory):
    """Test that function returns dict with correct keys and values."""
    result = read_csvs_to_dict(str(csv_directory))

    assert isinstance(result, dict)
    assert set(result.keys()) == {"users", "products"}


def test_read_csvs_to_dict_parses_rows_correctly(csv_directory):
    """Test that CSV rows are parsed as list of dictionaries."""
    result = read_csvs_to_dict(str(csv_directory))

    assert result["users"] == [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]
    assert result["products"] == [
        {"id": "1", "name": "Apple", "price": "1.50"},
        {"id": "2", "name": "Banana", "price": "0.75"},
    ]


def test_read_csvs_to_dict_empty_directory(tmp_path):
    """Test that function returns empty dict for directory with no CSVs."""
    result = read_csvs_to_dict(str(tmp_path))

    assert result == {}


def test_read_csvs_to_dict_ignores_non_csv_files(tmp_path):
    """Test that function ignores non-CSV files."""
    (tmp_path / "data.csv").write_text("col1\nval1\n")
    (tmp_path / "readme.txt").write_text("some text")
    (tmp_path / "data.json").write_text('{"key": "value"}')

    result = read_csvs_to_dict(str(tmp_path))

    assert list(result.keys()) == ["data"]


def test_read_csvs_to_dict_invalid_directory():
    """Test that function raises ValueError for invalid directory."""
    with pytest.raises(ValueError, match="is not a valid directory"):
        read_csvs_to_dict("/nonexistent/path")
