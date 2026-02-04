#!/usr/bin/env python3
"""Analyze transaction data from DataFrames."""

import argparse
import re
from dataclasses import dataclass
from pyexpat.errors import messages

import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe


@dataclass
class Transaction:
    date: str
    symbol: str
    type: str
    share_amount: int
    total_amount: float


def parse_transactions(df: pd.DataFrame) -> list[Transaction]:
    """Parse buy/sell transactions into Transaction objects.

    Args:
        df: DataFrame with 'Kirjauspäivä' and 'Viesti' columns.
            Viesti format: "O:SYMBOL /amount" or "M:SYMBOL /amount"

    Returns:
        List of Transaction objects.
    """
    transactions = []
    pattern = r"^([OM]):(\w+)\s*/(\d+)"

    for _, row in df.iterrows():
        viesti = row["Viesti"].strip()
        match = re.match(pattern, viesti)
        if match:
            type_code = match.group(1)
            symbol = match.group(2)
            share_amount = int(match.group(3))
            transaction_type = "BUY" if type_code == "O" else "SELL"
            total_amount = float(row["Määrä EUROA"].replace(",", "."))

            transactions.append(Transaction(
                date=row["Kirjauspäivä"],
                symbol=symbol,
                type=transaction_type,
                share_amount=share_amount,
                total_amount=abs(total_amount)
            ))

    return transactions


def calculate_fifo_profit(transactions: list[Transaction]) -> float:
    """Calculate profit from transactions using FIFO method.

    Args:
        transactions: List of Transaction objects sorted by date.

    Returns:
        Total profit (positive) or loss (negative).
    """
    buy_queue: list[tuple[int, float]] = []  # (shares, cost_per_share)
    total_profit = 0.0

    for tx in transactions:
        if tx.type == "BUY":
            cost_per_share = tx.total_amount / tx.share_amount
            buy_queue.append((tx.share_amount, cost_per_share))
        elif tx.type == "SELL":
            sell_price_per_share = tx.total_amount / tx.share_amount
            shares_to_sell = tx.share_amount

            while shares_to_sell > 0 and buy_queue:
                buy_shares, buy_cost = buy_queue[0]

                if buy_shares <= shares_to_sell:
                    profit = buy_shares * (sell_price_per_share - buy_cost)
                    total_profit += profit
                    shares_to_sell -= buy_shares
                    buy_queue.pop(0)
                else:
                    profit = shares_to_sell * (sell_price_per_share - buy_cost)
                    total_profit += profit
                    buy_queue[0] = (buy_shares - shares_to_sell, buy_cost)
                    shares_to_sell = 0

    return total_profit


def find_dividend_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Find rows where Laji is 'Arvopaperit' (stock tradings).

    Args:
        df: DataFrame containing a 'Laji' column.

    Returns:
        DataFrame with only rows where Laji == 'Arvopaperit'.
    """
    return df[df["Selitys"].str.lower() == "arvopaperit"]
def find_service_charge_transactions(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Selitys"].str.lower() == "palvelumaksu"]


def find_transactions_by_ticker_symbol(df: pd.DataFrame, ticker_symbol: str) -> pd.DataFrame:
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
    print("Total service charges")
    sc = find_service_charge_transactions(df)
    print(sc)
    print(sum_field(sc, "Määrä EUROA"))
    mrn_trs_dfs = find_transactions_by_ticker_symbol(df, "MRNA")
    print(mrn_trs_dfs)
    mr_trs = parse_transactions(mrn_trs_dfs)
    print(mr_trs)



if __name__ == "__main__":
    main()
