#!/usr/bin/env python3
"""Unit tests for transaction_filters module."""

import pandas as pd

from transaction_filters import find_expenses, match_trading


def test_find_expenses():
    """
    700,TILISIIRTO,, is expense
    700,NOSTO,O:PFE US /30, is purchase of stock

    """
    df = pd.DataFrame({
        "Määrä EUROA": ["-15,49", "-625,7"],
        "Laji": [700, 700],
        "Selitys": ["TILISIIRTO", "NOSTO"],
        "Viesti": ["", "O:PFE US /30"]
    })
    result = find_expenses(df)
    assert len(result) == 1
    item = result.iloc[0]
    assert item["Laji"] == 700
    assert item["Määrä EUROA"] == "-15,49"



def test_match_trading_buy():
    """Test matching a buy transaction."""
    match = match_trading("O:MRNA /20")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "MRNA"
    assert match.group(3) == "20"


def test_match_trading_buy_with_country_code():
    """Test matching a buy transaction."""
    match = match_trading("O:PFE US /100")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "PFE"
    assert match.group(3) == "100"


def test_match_trading_buy_stock_with_symbol_containing_dot():
    """Test matching a sell transaction."""
    match = match_trading("O:STZ.N /4")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "STZ.N"
    assert match.group(3) == "4"

def test_match_trading_sell():
    """Test matching a sell transaction."""
    match = match_trading("M:SIRI /100")
    assert match is not None
    assert match.group(1) == "M"
    assert match.group(2) == "SIRI"
    assert match.group(3) == "100"


def test_match_trading_invalid():
    """Test that invalid messages don't match."""
    assert match_trading("invalid") is None
    assert match_trading("X:MRNA /20") is None
    assert match_trading("O:MRNA") is None