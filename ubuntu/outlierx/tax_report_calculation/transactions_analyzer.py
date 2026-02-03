#!/usr/bin/env python3
"""Analyze transaction data from DataFrames."""

import argparse

import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe


def find_dividend_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Find rows where Laji is 'Arvopaperit' (stock tradings).

    Args:
        df: DataFrame containing a 'Laji' column.

    Returns:
        DataFrame with only rows where Laji == 'Arvopaperit'.
    """
    return df[df["Selitys"].str.lower() == "arvopaperit"]


def sum_field(df: pd.DataFrame, field: str) -> float:
    """Sum values of a field in a DataFrame.

    Args:
        df: DataFrame containing the field.
        field: Column name to sum.

    Returns:
        Sum of the field values.
    """
    values = df[field].str.replace(",", ".").astype(float)
    return values.sum()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    stock_tradings = find_dividend_transactions(df)

    print(f"Found {len(stock_tradings)} stock trading(s):")
    print(stock_tradings)
    print("Total dividend:")
    print(sum_field(stock_tradings, "Määrä EUROA"))


if __name__ == "__main__":
    main()
