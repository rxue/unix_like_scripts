#!/usr/bin/env python3
"""Unit tests for transactions_analyzer module."""

from transactions_analyzer import Lot, stock_trading_profit_in_fifo


def test_stock_trading_profit_in_fifo_base():
    """Buy 10 shares at $10, sell 10 shares at $15 = $50 profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=10, total_amount=100.0),
        Lot(date="2024-01-02", type="SELL", share_amount=10, total_amount=150.0),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 50.0


def test_stock_trading_profit_in_fifo_order():
    transactions = [
        Lot(date="2024-01-13", type="BUY", share_amount=20, total_amount=574.68),
        Lot(date="2024-01-13", type="BUY", share_amount=20, total_amount=575.96),
        Lot(date="2024-01-30", type="SELL", share_amount=20, total_amount=612),
    ]
    # 612-574.68 = $37.32 profit
    assert stock_trading_profit_in_fifo(transactions)[0] == 37.32


def test_partial_sell_from_single_buy():
    """Buy 20 shares at $10, sell 10 at $15 = $50 profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=20, total_amount=200.0),
        Lot(date="2024-01-02", type="SELL", share_amount=10, total_amount=150.0),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 50.0


def test_sell_across_multiple_buys():
    """Buy 5 at $10, buy 10 at $20, sell 10 at $25."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=5, total_amount=50.0),
        Lot(date="2024-01-02", type="BUY", share_amount=10, total_amount=200.0),
        Lot(date="2024-01-03", type="SELL", share_amount=10, total_amount=250.0),
    ]
    # Sell 5 from first batch: 5 * ($25 - $10) = $75
    # Sell 5 from second batch: 5 * ($25 - $20) = $25
    # Total profit = $100
    assert stock_trading_profit_in_fifo(transactions)[0] == 100.0


def test_no_transactions():
    """Empty transaction list returns zero profit."""
    transactions = []
    assert stock_trading_profit_in_fifo(transactions)[0] == 0.0


def test_only_buys():
    """Only buy transactions, no sells = zero realized profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=10, total_amount=100.0),
        Lot(date="2024-01-02", type="BUY", share_amount=10, total_amount=200.0),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 0.0
