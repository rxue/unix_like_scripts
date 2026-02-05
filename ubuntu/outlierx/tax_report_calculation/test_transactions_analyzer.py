#!/usr/bin/env python3
"""Unit tests for transactions_analyzer module."""

from transactions_analyzer import Transaction, calculate_fifo_profit


def test_simple_profit():
    """Buy 10 shares at $10, sell 10 shares at $15 = $50 profit."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=10, total_amount=100.0),
        Transaction(date="2024-01-02", symbol="TEST", type="SELL", share_amount=10, total_amount=150.0),
    ]
    assert calculate_fifo_profit(transactions) == 50.0


def test_simple_loss():
    """Buy 10 shares at $10, sell 10 shares at $8 = $20 loss."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=10, total_amount=100.0),
        Transaction(date="2024-01-02", symbol="TEST", type="SELL", share_amount=10, total_amount=80.0),
    ]
    assert calculate_fifo_profit(transactions) == -20.0


def test_fifo_order():
    """Buy 10 at $10, buy 10 at $20, sell 10 at $15. FIFO sells first batch."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=10, total_amount=100.0),
        Transaction(date="2024-01-02", symbol="TEST", type="BUY", share_amount=10, total_amount=200.0),
        Transaction(date="2024-01-03", symbol="TEST", type="SELL", share_amount=10, total_amount=150.0),
    ]
    # Sell 10 shares at $15, cost was $10 (first batch) = $50 profit
    assert calculate_fifo_profit(transactions) == 50.0


def test_partial_sell_from_single_buy():
    """Buy 20 shares at $10, sell 10 at $15 = $50 profit."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=20, total_amount=200.0),
        Transaction(date="2024-01-02", symbol="TEST", type="SELL", share_amount=10, total_amount=150.0),
    ]
    assert calculate_fifo_profit(transactions) == 50.0


def test_sell_across_multiple_buys():
    """Buy 5 at $10, buy 10 at $20, sell 10 at $25."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=5, total_amount=50.0),
        Transaction(date="2024-01-02", symbol="TEST", type="BUY", share_amount=10, total_amount=200.0),
        Transaction(date="2024-01-03", symbol="TEST", type="SELL", share_amount=10, total_amount=250.0),
    ]
    # Sell 5 from first batch: 5 * ($25 - $10) = $75
    # Sell 5 from second batch: 5 * ($25 - $20) = $25
    # Total profit = $100
    assert calculate_fifo_profit(transactions) == 100.0


def test_no_transactions():
    """Empty transaction list returns zero profit."""
    transactions = []
    assert calculate_fifo_profit(transactions) == 0.0


def test_only_buys():
    """Only buy transactions, no sells = zero realized profit."""
    transactions = [
        Transaction(date="2024-01-01", symbol="TEST", type="BUY", share_amount=10, total_amount=100.0),
        Transaction(date="2024-01-02", symbol="TEST", type="BUY", share_amount=10, total_amount=200.0),
    ]
    assert calculate_fifo_profit(transactions) == 0.0
