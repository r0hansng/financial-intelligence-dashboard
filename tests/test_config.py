"""Tests for configuration module."""

import pytest
from src.utils.config import TICKERS, TRADING_DAYS, RISK_FREE_RATE


class TestConfig:
    """Test configuration values."""

    def test_tickers_is_list(self):
        """Test that TICKERS is a list."""
        assert isinstance(TICKERS, list), "TICKERS should be a list"

    def test_tickers_not_empty(self):
        """Test that TICKERS list is not empty."""
        assert len(TICKERS) > 0, "TICKERS list should not be empty"

    def test_tickers_are_strings(self):
        """Test that all tickers are strings."""
        for ticker in TICKERS:
            assert isinstance(ticker, str), f"Ticker {ticker} should be a string"

    def test_tickers_have_expected_values(self):
        """Test that TICKERS contains expected values."""
        expected_tickers = {"AAPL", "MSFT", "GOOGL", "^GSPC"}
        actual_tickers = set(TICKERS)
        assert actual_tickers == expected_tickers, f"TICKERS should contain {expected_tickers}"

    def test_trading_days_is_positive_integer(self):
        """Test that TRADING_DAYS is a positive integer."""
        assert isinstance(TRADING_DAYS, int), "TRADING_DAYS should be an integer"
        assert TRADING_DAYS > 0, "TRADING_DAYS should be positive"

    def test_trading_days_reasonable_value(self):
        """Test that TRADING_DAYS has a reasonable value."""
        assert 200 <= TRADING_DAYS <= 270, "TRADING_DAYS should be around 252"

    def test_risk_free_rate_is_numeric(self):
        """Test that RISK_FREE_RATE is numeric."""
        assert isinstance(RISK_FREE_RATE, (int, float)), "RISK_FREE_RATE should be numeric"

    def test_risk_free_rate_reasonable_value(self):
        """Test that RISK_FREE_RATE has a reasonable value."""
        assert 0 <= RISK_FREE_RATE <= 1, "RISK_FREE_RATE should be between 0 and 1"
