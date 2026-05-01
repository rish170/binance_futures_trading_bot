import pytest
from trading_bot.bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

def test_validate_symbol():
    assert validate_symbol("BTCUSDT") == "BTCUSDT"
    with pytest.raises(ValueError, match="Symbol must be an uppercase string"):
        validate_symbol("btcusdt")
    with pytest.raises(ValueError, match="Symbol must be a non-empty string"):
        validate_symbol("")

def test_validate_side():
    assert validate_side("buy") == "BUY"
    assert validate_side("SELL") == "SELL"
    with pytest.raises(ValueError, match="Side must be either 'BUY' or 'SELL'"):
        validate_side("HOLD")

def test_validate_order_type():
    assert validate_order_type("market") == "MARKET"
    assert validate_order_type("LIMIT") == "LIMIT"
    with pytest.raises(ValueError, match="Order type must be either 'MARKET' or 'LIMIT'"):
        validate_order_type("STOP_LOSS")

def test_validate_quantity():
    assert validate_quantity(0.001) == 0.001
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        validate_quantity(0)
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        validate_quantity(-1.5)

def test_validate_price():
    # Price is not required for MARKET
    assert validate_price("MARKET") is None
    assert validate_price("MARKET", 50000) == 50000
    
    # Price is required for LIMIT
    assert validate_price("LIMIT", 50000) == 50000
    with pytest.raises(ValueError, match="Price is required and must be > 0 for LIMIT orders"):
        validate_price("LIMIT")
    with pytest.raises(ValueError, match="Price is required and must be > 0 for LIMIT orders"):
        validate_price("LIMIT", 0)
    with pytest.raises(ValueError, match="Price is required and must be > 0 for LIMIT orders"):
        validate_price("LIMIT", -100)
