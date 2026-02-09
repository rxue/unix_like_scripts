#!/usr/bin/env python3
"""Read all CSV files from a directory into a pandas DataFrame."""

from pathlib import Path

import pandas as pd


def read_csvs_to_dataframe(directory: str) -> pd.DataFrame:
    """Read all CSV files in a directory and return as a DataFrame.

    All CSV files must have the same columns in the same order.

    Args:
        directory: Path to the directory containing CSV files.

    Returns:
        DataFrame containing all rows from all CSV files.
    """
    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise ValueError(f"'{directory}' is not a valid directory")

    dfs = [pd.read_csv(f, encoding="latin-1", sep=";") for f in sorted(dir_path.glob("*.csv"))]

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)
