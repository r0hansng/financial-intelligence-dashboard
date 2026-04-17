"""Pytest configuration and fixtures."""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_returns():
    """Fixture providing sample returns data."""
    return pd.Series(np.random.normal(0.001, 0.015, 252))


@pytest.fixture
def sample_dataframe():
    """Fixture providing sample DataFrame with financial data."""
    return pd.DataFrame({
        "date": pd.date_range("2020-01-01", periods=252),
        "ticker": ["AAPL"] * 252,
        "returns": np.random.normal(0.001, 0.015, 252),
        "price": np.random.normal(100, 10, 252)
    })


@pytest.fixture
def sample_multi_ticker_dataframe():
    """Fixture providing sample DataFrame with multiple tickers."""
    dates = pd.date_range("2020-01-01", periods=252)
    tickers = ["AAPL", "MSFT", "GOOGL", "^GSPC"]
    
    data = []
    for ticker in tickers:
        for date in dates:
            data.append({
                "date": date,
                "ticker": ticker,
                "returns": np.random.normal(0.001, 0.015),
                "price": np.random.normal(100, 10)
            })
    
    return pd.DataFrame(data)
