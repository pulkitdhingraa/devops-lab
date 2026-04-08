# Write pytest tests for this function:

# def calculate_pnl(entry: float, exit: float, qty: float, side: str) -> float

# Write tests for:
# 1. A profitable long (buy low, sell high)
# 2. A losing long
# 3. A profitable short (sell high, buy back low)
# 4. side = "invalid" should raise ValueError
# 5. qty <= 0 should raise ValueError

import pytest
from unittest.mock import patch, Mock

def calculate_pnl(entry, exit, qty, side): 
    if side not in ("buy", "sell"):
        raise ValueError(f"invalid side: {side}, must be 'buy' or 'sell'")
    if qty <= 0:
        raise ValueError(f"qty must be postive, got {qty}")
    
    if side == "buy":
        return (exit-entry)*qty 
    else:
        return (entry-exit)*qty

def test_profitable_long():
    result = calculate_pnl(entry=40, exit=60, qty=1.0, side="buy")
    assert result == 20.0

def test_losing_long():
    result = calculate_pnl(entry=40, exit=20, qty=1.0, side="buy")
    assert result == -20.0

def test_profitable_short():
    result = calculate_pnl(entry=40, exit=20, qty=1.0, side="sell")
    assert result == 20.0

def test_invalid_side():
    with pytest.raises(ValueError):
        calculate_pnl(entry=20,exit=40,qty=1.0,side="invalid")

def test_invalid_qty():
    with pytest.raises(ValueError):
        calculate_pnl(entry=20,exit=40,qty=0,side="buy")


###### Another Example #######
def test_fetch_price_success():
    mock_response = Mock()
    mock_response.json.return_value = {"price": 40.0}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        price = fetch_price("BTC")
    assert price == 40.0

def test_fetch_price_missing_field():
    mock_response = Mock()
    mock_response.json.return_value = {"bid": 40.0}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(PriceFetchError, match="missing price field"):
            fetch_price("BTC")

def test_fetch_price_timeout():
    with patch("requests.get", side_effect=requests.Timeout()):
        with pytest.raises(PriceFetchError, match="timeout"):
            fetch_price("BTC")

# Key Learnings
# don't just test the happy path
# What breaks in prod at 3am is the timeout, the missing field, the 503. Write tests for those.