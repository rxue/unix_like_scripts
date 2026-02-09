#!/usr/bin/env python3
"""Analyze transaction data from DataFrames."""

import argparse
import re
from dataclasses import dataclass

import pandas as pd

from csv_to_dataframe import read_csvs_to_dataframe
from transaction_filters import (
    find_dividend_payments,
    find_all_stock_tradings_by_symbol,
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
    financial_asset: float


def transfer_transactions_to_lots(df: pd.DataFrame) -> list[Lot]:
    """Parse buy/sell transactions into Transaction objects.

    Args:
        df: DataFrame with 'Kirjauspäivä' and 'Viesti' columns.
            Viesti format: "O:SYMBOL /amount" or "M:SYMBOL /amount"

    Returns:
        List of Transaction objects.
    """
    transactions = []

    for _, row in df.iterrows():
        viesti = row["Viesti"].strip()
        match = _match_trading(viesti)
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


def _match_trading(viesti: str) -> re.Match[str] | None:
    pattern = r"^([OM]):(\w+)(?:\s+\w+)?\s*/(\d+)"
    return re.match(pattern, viesti)


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
    def stock_trading_profit_and_book_values_by_symbol(all_tradings: dict[str, pd.DataFrame]) -> dict[str, tuple[float, float]]:
        """Calculate capital gains and book values of each Stock.

        Args:
            all_tradings: all the stock trading transactions

        Returns:
            map whose key is the stock symbol, and the value is the (profit, book_value)
        """
        result = {}
        for symbol, symbol_df in all_tradings.items():
            lots = transfer_transactions_to_lots(symbol_df)
            profit, remaining_lots = stock_trading_profit_in_fifo(lots)
            book_value = sum(lot.total_amount for lot in remaining_lots)
            result[symbol] = (profit, book_value)
        return result

    all_tradings_by_symbol = find_all_stock_tradings_by_symbol(df)
    trading_profit_and_book_values = stock_trading_profit_and_book_values_by_symbol(all_tradings_by_symbol)
    total_trading_profit = sum(profit for profit, _ in trading_profit_and_book_values.values())
    dividend_payments_df = find_dividend_payments(df)
    business_income = sum_money(pd.concat([dividend_payments_df])) + total_trading_profit

    # Business expenses: negative amounts excluding stock trading (Laji != 700)
    expenses_df = find_expenses(df)
    business_expense = abs(sum_money(expenses_df))

    total_financial_asset = sum(book_value for _, book_value in trading_profit_and_book_values.values())

    return Report(
        business_income=business_income,
        business_expense=business_expense,
        cash=sum_money(df),
        financial_asset=total_financial_asset
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
