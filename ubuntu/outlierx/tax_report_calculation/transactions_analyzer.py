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
    find_by_ticker_symbol,
    find_stock_tradings,
    find_expenses,
)


@dataclass
class Lot:
    date: str
    type: str
    share_amount: int
    total_amount: float


@dataclass
class Report:
    business_income: float
    business_expense: float
    cash: float


def parse_transactions(df: pd.DataFrame) -> list[Lot]:
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
            share_amount = int(match.group(3))
            transaction_type = "BUY" if type_code == "O" else "SELL"
            total_amount = float(row["Määrä EUROA"].replace(",", "."))

            transactions.append(Lot(
                date=row["Kirjauspäivä"],
                type=transaction_type,
                share_amount=share_amount,
                total_amount=abs(total_amount)
            ))

    return transactions


def stock_trading_profit_in_fifo(transactions: list[Lot]) -> (float, list[Lot]):
    """Calculate profit from transactions using FIFO method.

    Args:
        transactions: List of Lot objects sorted by date.

    Returns:
        profit: Total profit (positive) or loss (negative)
        remaining_lots: List of Lot for unsold shares
    """
    buy_queue: list[tuple[str, int, int]] = []  # (date, shares, total_cost_in_cents)
    total_profit_cents = 0

    for tx in transactions:
        total_cents = round(tx.total_amount * 100)
        if tx.type == "BUY":
            buy_queue.append((tx.date, tx.share_amount, total_cents))
        elif tx.type == "SELL":
            sell_total_cents = total_cents
            shares_to_sell = tx.share_amount

            while shares_to_sell > 0 and buy_queue:
                buy_date, buy_shares, buy_total_cents = buy_queue[0]

                if buy_shares <= shares_to_sell:
                    sell_portion_cents = sell_total_cents * buy_shares // shares_to_sell
                    total_profit_cents += sell_portion_cents - buy_total_cents
                    sell_total_cents -= sell_portion_cents
                    shares_to_sell -= buy_shares
                    buy_queue.pop(0)
                else:
                    buy_portion_cents = buy_total_cents * shares_to_sell // buy_shares
                    total_profit_cents += sell_total_cents - buy_portion_cents
                    buy_queue[0] = (buy_date, buy_shares - shares_to_sell, buy_total_cents - buy_portion_cents)
                    shares_to_sell = 0

    remaining_lots = [Lot(date=date, type="BUY", share_amount=shares, total_amount=cost_in_cents / 100) for date, shares, cost_in_cents in buy_queue]
    return total_profit_cents / 100, remaining_lots


def calculate_capital_gains(df: pd.DataFrame) -> float:
    """Calculate total capital gains from all stock trading transactions.

    Args:
        df: DataFrame containing transaction data.

    Returns:
        Total capital gains with FIFO.
    """
    stock_tradings_df = find_stock_tradings(df)

    # Extract unique stock symbols from Viesti field (format: O:SYMBOL or M:SYMBOL)
    pattern = r"^[OM]:(\w+)"
    symbols = set()
    for viesti in stock_tradings_df["Viesti"].str.strip():
        match = re.match(pattern, viesti)
        if match:
            symbols.add(match.group(1))
    # Calculate profit for each symbol and sum
    total_capital_gains_cents = 0
    for symbol in symbols:
        symbol_df = find_by_ticker_symbol(df, symbol)
        transactions = parse_transactions(symbol_df)
        profit, _ = stock_trading_profit_in_fifo(transactions)
        total_capital_gains_cents += round(profit * 100)
    return total_capital_gains_cents / 100


def sum_money(df: pd.DataFrame) -> float:
    """Sum money values in a DataFrame using cents for precision.

    Args:
        df: DataFrame containing 'Määrä EUROA' column.

    Returns:
        Sum of the money values.
    """
    values = df["Määrä EUROA"].str.replace(",", ".").astype(float)
    cents = (values * 100).round().astype(int)
    return cents.sum() / 100


def tax_report(df: pd.DataFrame) -> Report:
    """Generate a tax report with business income and expenses.

    Args:
        df: DataFrame containing transaction data.

    Returns:
        Report object with business income and expenses.
    """
    # Business income: positive amounts excluding stock trading (Laji != 700)
    income_df = find_stock_tradings(df)
    capital_gains = calculate_capital_gains(income_df)
    dividend_payments = find_dividend_payments(df)
    business_income = sum_money(pd.concat([dividend_payments])) + capital_gains

    # Business expenses: negative amounts excluding stock trading (Laji != 700)
    expenses_df = find_expenses(df)
    business_expense = abs(sum_money(expenses_df))

    return Report(
        business_income=business_income,
        business_expense=business_expense,
        cash=sum_money(df)
    )


def main():
    parser = argparse.ArgumentParser(
        description="Analyze transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(tax_report(df))


if __name__ == "__main__":
    main()
