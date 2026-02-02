#!/usr/bin/env python3
"""Read all CSV files from a directory and combine them into one dictionary."""

import argparse
import csv
from pathlib import Path


def read_csvs_to_dict(directory: str) -> dict:
    """Read all CSV files in a directory and return them as a dictionary.

    Args:
        directory: Path to the directory containing CSV files.

    Returns:
        Dictionary with filenames (without extension) as keys and
        list of row dictionaries as values.
    """
    result = {}
    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise ValueError(f"'{directory}' is not a valid directory")

    for csv_file in dir_path.glob("*.csv"):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            result[csv_file.stem] = list(reader)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Read all CSV files from a directory into a dictionary"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    data = read_csvs_to_dict(args.directory)

    print(f"Loaded {len(data)} CSV file(s):")
    for filename, rows in data.items():
        print(f"  - {filename}: {len(rows)} row(s)")


if __name__ == "__main__":
    main()
