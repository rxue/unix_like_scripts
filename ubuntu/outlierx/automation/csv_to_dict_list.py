#!/usr/bin/env python3
"""Read all CSV files from a directory into a single list of dicts."""

import csv
from pathlib import Path


def read_csvs_to_list(directory: str) -> list[dict]:
    """Read all CSV files in a directory and return as a list of dicts.

    All CSV files must have the same columns in the same order.

    Args:
        directory: Path to the directory containing CSV files.

    Returns:
        List of dictionaries where each dict represents a row.
    """
    result = []
    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise ValueError(f"'{directory}' is not a valid directory")

    for csv_file in dir_path.glob("*.csv"):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result.append(row)

    return result
