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


def find_all_stock_tradings_by_symbol(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Find stock trading transactions grouped by ticker symbol.

    Args:
        df: DataFrame containing 'Laji' and 'Viesti' columns.

    Returns:
        Dict with stock symbol as key and DataFrame of transactions as value.
    """
    symbol_to_row_index_list_map: dict[str, list[int]] = {}

    for idx, row in df.iterrows():
        if row["Laji"] != 700:
            continue
        viesti = row["Viesti"].strip()
        match = match_trading(viesti)
        if match:
            symbol = match.group(1)
            if symbol not in symbol_to_row_index_list_map:
                symbol_to_row_index_list_map[symbol] = []
            symbol_to_row_index_list_map[symbol].append(idx)

    return {symbol: df.loc[indices] for symbol, indices in symbol_to_row_index_list_map.items()}


def match_trading(viesti: str) -> re.Match[str] | None:
    pattern = r"^([OM]):([\w.]+)(?:\s+\w+)?\s*/(\d+)"
    return re.match(pattern, viesti)


def find_cash_infusion(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["Laji"] == 710) & (df["Selitys"].str.strip().str.lower() == "tilisiirto")]


def find_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Find expense rows, i.e. Määrä EUROA is negative and not a stock trading.

    Args:
        df: DataFrame containing 'Määrä EUROA' and 'Viesti' columns.

    Returns:
        DataFrame with only rows where amount is negative and Viesti doesn't match a trading pattern.
    """
    amounts = df["Määrä EUROA"].str.replace(",", ".").astype(float)
    negative = df[amounts < 0]
    is_trading = negative["Viesti"].apply(lambda v: match_trading(v.strip()) is not None)
    return negative[~is_trading]


def main():
    parser = argparse.ArgumentParser(
        description="Filter transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(f"Total rows: {len(df)}")
    cash_infusions = find_cash_infusion(df)
    dividend_payments = find_dividend_payments(df)
    expenses = find_expenses(df)
    stock_tradings_by_symbol = find_all_stock_tradings_by_symbol(df)
    total_stock_trading_rows = sum(len(symbol_df) for symbol_df in stock_tradings_by_symbol.values())
    print(f"total stock trading rows is {total_stock_trading_rows}")
    whole_sum = total_stock_trading_rows + len(dividend_payments) + len(expenses) + len(cash_infusions)
    if len(df) > 1 and len(df) == whole_sum:
        print("check sum passed")
    else:
        print("WARNING: check sum failed!")


if __name__ == "__main__":
    main()
