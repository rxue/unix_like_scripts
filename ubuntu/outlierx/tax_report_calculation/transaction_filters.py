#!/usr/bin/env python3
"""Filter functions for transaction DataFrames."""

import argparse
import re

import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe


def find_dividend_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Find rows where Laji is 'Arvopaperit' (stock tradings).

    Args:
        df: DataFrame containing a 'Laji' column.

    Returns:
        DataFrame with only rows where Laji == 'Arvopaperit'.
    """
    return df[df["Selitys"].str.lower() == "arvopaperit"]


def find_service_charges(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Selitys"].str.lower() == "palvelumaksu"]


def find_stock_tradings(df: pd.DataFrame) -> pd.DataFrame:
    """Find stock trading transactions (buy/sell), excluding dividends.

    Args:
        df: DataFrame containing 'Laji' column.

    Returns:
        DataFrame with only stock trading rows (Laji == 700).
    """
    return df[df["Laji"] == 700]


def find_all_stock_tradings_by_symbol(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Find stock trading transactions grouped by ticker symbol.

    Args:
        df: DataFrame containing 'Laji' and 'Viesti' columns.

    Returns:
        Dict with stock symbol as key and DataFrame of transactions as value.
    """
    pattern = r"^[OM]:(\w+)"
    symbol_to_row_index_list_map: dict[str, list[int]] = {}

    for idx, row in df.iterrows():
        if row["Laji"] != 700:
            continue
        viesti = row["Viesti"].strip()
        match = re.match(pattern, viesti)
        if match:
            symbol = match.group(1)
            if symbol not in symbol_to_row_index_list_map:
                symbol_to_row_index_list_map[symbol] = []
            symbol_to_row_index_list_map[symbol].append(idx)

    return {symbol: df.loc[indices] for symbol, indices in symbol_to_row_index_list_map.items()}


def find_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Find expense rows, i.e. Määrä EUROA is negative and Laji is not 700.

    Args:
        df: DataFrame containing 'Määrä EUROA' and 'Laji' columns.

    Returns:
        DataFrame with only rows where amount is negative and Laji != 700.
    """
    amounts = df["Määrä EUROA"].str.replace(",", ".").astype(float)
    return df[(amounts < 0) & (df["Laji"] != 700)]


def main():
    parser = argparse.ArgumentParser(
        description="Filter transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(df)
    print("********************************************************")
    stock_tradings_dict = find_all_stock_tradings_by_symbol(df)
    for symbol, symbol_df in stock_tradings_dict.items():
        print(symbol)
        print(symbol_df)
        print("================================================")


if __name__ == "__main__":
    main()
