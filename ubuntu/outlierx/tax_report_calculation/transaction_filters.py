#!/usr/bin/env python3
"""Filter functions for transaction DataFrames."""

import pandas as pd


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


def find_by_ticker_symbol(df: pd.DataFrame, ticker_symbol: str) -> pd.DataFrame:
    """Find transactions where Laji is 700 and Viesti starts with O:<ticker> or M:<ticker>.

    Args:
        df: DataFrame containing 'Laji' and 'Viesti' columns.
        ticker_symbol: Stock ticker symbol to filter by.

    Returns:
        DataFrame with matching transactions.
    """
    category_code_filter = df["Laji"] == 700
    viesti_trimmed = df["Viesti"].str.strip()
    message_filter = viesti_trimmed.str.startswith(f"O:{ticker_symbol}") | viesti_trimmed.str.startswith(f"M:{ticker_symbol}")
    return df[category_code_filter & message_filter]
