#!/usr/bin/env python3
"""Unit tests for transactions_analyzer module."""

from transactions_analyzer import Lot, stock_trading_profit_in_fifo, _match_trading


def test_stock_trading_profit_in_fifo_base():
    """Buy 10 shares at $10, sell 10 shares at $15 = $50 profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=10, money_amount_in_cent=10000),
        Lot(date="2024-01-02", type="SELL", share_amount=10, money_amount_in_cent=15000),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 5000


def test_stock_trading_profit_in_fifo_order():
    lot_to_remain = Lot(date="2024-01-13", type="BUY", share_amount=20, money_amount_in_cent=57596)
    transactions = [
        Lot(date="2024-01-13", type="BUY", share_amount=20, money_amount_in_cent=57468),
        lot_to_remain,
        (Lot(date="2024-01-30", type="SELL", share_amount=20, money_amount_in_cent=61200)),
    ]
    profit, remaining_lots = stock_trading_profit_in_fifo(transactions)
    # 61200-57468 = 3732 cents profit
    assert profit == 3732
    assert remaining_lots == [lot_to_remain]



def test_partial_sell_from_single_buy():
    """Buy 20 shares at $10, sell 10 at $15 = $50 profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=20, money_amount_in_cent=20000),
        Lot(date="2024-01-02", type="SELL", share_amount=10, money_amount_in_cent=15000),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 5000


def test_sell_across_multiple_buys():
    """Buy 5 at $10, buy 10 at $20, sell 10 at $25."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=5, money_amount_in_cent=5000),
        Lot(date="2024-01-02", type="BUY", share_amount=10, money_amount_in_cent=20000),
        Lot(date="2024-01-03", type="SELL", share_amount=10, money_amount_in_cent=25000),
    ]
    # Sell 5 from first batch: 5 * (2500 - 1000) = 7500 cents
    # Sell 5 from second batch: 5 * (2500 - 2000) = 2500 cents
    # Total profit = 10000 cents
    assert stock_trading_profit_in_fifo(transactions)[0] == 10000


def test_no_transactions():
    """Empty transaction list returns zero profit."""
    transactions = []
    assert stock_trading_profit_in_fifo(transactions)[0] == 0


def test_only_buys():
    """Only buy transactions, no sells = zero realized profit."""
    transactions = [
        Lot(date="2024-01-01", type="BUY", share_amount=10, money_amount_in_cent=10000),
        Lot(date="2024-01-02", type="BUY", share_amount=10, money_amount_in_cent=20000),
    ]
    assert stock_trading_profit_in_fifo(transactions)[0] == 0


def test_match_trading_buy():
    """Test matching a buy transaction."""
    match = _match_trading("O:MRNA /20")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "MRNA"
    assert match.group(3) == "20"

def test_match_trading_buy_with_country_code():
    """Test matching a buy transaction."""
    match = _match_trading("O:PFE US /100")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "PFE"
    assert match.group(3) == "100"


def test_match_trading_sell():
    """Test matching a sell transaction."""
    match = _match_trading("M:SIRI /100")
    assert match is not None
    assert match.group(1) == "M"
    assert match.group(2) == "SIRI"
    assert match.group(3) == "100"


def test_match_trading_invalid():
    """Test that invalid messages don't match."""
    assert _match_trading("invalid") is None
    assert _match_trading("X:MRNA /20") is None
    assert _match_trading("O:MRNA") is None
