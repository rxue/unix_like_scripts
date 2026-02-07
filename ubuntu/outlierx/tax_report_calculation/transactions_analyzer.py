#!/usr/bin/env python3
"""Analyze transaction data from DataFrames."""

import argparse
import re
from dataclasses import dataclass
from pyexpat.errors import messages

import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe
from transaction_filters import (
    find_dividend_payments,
    find_service_charges,
    find_by_ticker_symbol,
    find_stock_tradings
)


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


def calculate_profit_in_fifo(transactions: list[Transaction]) -> float:
    """Calculate profit from transactions using FIFO method.

    Args:
        transactions: List of Transaction objects sorted by date.

    Returns:
        Total profit (positive) or loss (negative).
    """
    buy_queue: list[tuple[int, int]] = []  # (shares, total_cost_in_cents)
    total_profit_cents = 0

    for tx in transactions:
        total_cents = round(tx.total_amount * 100)
        if tx.type == "BUY":
            buy_queue.append((tx.share_amount, total_cents))
        elif tx.type == "SELL":
            sell_total_cents = total_cents
            shares_to_sell = tx.share_amount

            while shares_to_sell > 0 and buy_queue:
                buy_shares, buy_total_cents = buy_queue[0]

                if buy_shares <= shares_to_sell:
                    sell_portion_cents = sell_total_cents * buy_shares // shares_to_sell
                    total_profit_cents += sell_portion_cents - buy_total_cents
                    sell_total_cents -= sell_portion_cents
                    shares_to_sell -= buy_shares
                    buy_queue.pop(0)
                else:
                    buy_portion_cents = buy_total_cents * shares_to_sell // buy_shares
                    total_profit_cents += sell_total_cents - buy_portion_cents
                    buy_queue[0] = (buy_shares - shares_to_sell, buy_total_cents - buy_portion_cents)
                    shares_to_sell = 0

    return total_profit_cents / 100


def sum_money(df: pd.DataFrame, field: str) -> float:
    """Sum values of a field in a DataFrame using cents for precision.

    Args:
        df: DataFrame containing the field.
        field: Column name to sum.

    Returns:
        Sum of the field values.
    """
    values = df[field].str.replace(",", ".").astype(float)
    cents = (values * 100).round().astype(int)
    return cents.sum() / 100


def main():
    parser = argparse.ArgumentParser(
        description="Analyze transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(f"SUM: {sum_money(df, "Määrä EUROA")}")
    stock_tradings = find_dividend_payments(df)

    print(f"Found {len(stock_tradings)} stock trading(s):")
    print(stock_tradings)
    print("Total dividend:")
    print(sum_money(stock_tradings, "Määrä EUROA"))
    print("Total service charges")
    sc = find_service_charges(df)
    print(sc)
    print(sum_money(sc, "Määrä EUROA"))
    mrn_trs_dfs = find_by_ticker_symbol(df, "MRNA")
    print(mrn_trs_dfs)
    mr_trs = parse_transactions(mrn_trs_dfs)
    print(mr_trs)
    mrn_profit = calculate_profit_in_fifo(mr_trs)
    print(f"profit {mrn_profit}")
    stock_tradings = find_stock_tradings(df)
    print(stock_tradings)
    print(f"Financial asset (book value of stock shares) {sum_money(stock_tradings, "Määrä EUROA")}")


if __name__ == "__main__":
    main()
