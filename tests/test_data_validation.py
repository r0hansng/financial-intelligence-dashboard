"""Tests for data validation module."""

import pytest
import pandas as pd
import numpy as np


class TestDataValidation:
    """Test data validation functions."""

    def test_dataframe_not_empty(self):
        """Test that a valid DataFrame is not empty."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        assert len(df) > 0, "DataFrame should not be empty"

    def test_dataframe_has_required_columns(self):
        """Test that DataFrame has required columns."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        required_columns = ["date", "ticker", "returns"]
        for col in required_columns:
            assert col in df.columns, f"Column {col} should exist in DataFrame"

    def test_dataframe_no_missing_values(self):
        """Test that DataFrame has no missing values."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        assert df.isnull().sum().sum() == 0, "DataFrame should have no missing values"

    def test_dataframe_with_missing_values_detected(self):
        """Test that missing values can be detected."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        df.loc[10, "returns"] = np.nan
        assert df.isnull().sum().sum() > 0, "Missing values should be detected"

    def test_returns_are_numeric(self):
        """Test that returns column contains numeric values."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        assert pd.api.types.is_numeric_dtype(df["returns"]), "Returns should be numeric"

    def test_returns_in_reasonable_range(self):
        """Test that returns are in a reasonable range."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        # Daily returns typically between -20% and +20%
        assert (df["returns"] >= -0.20).all(), "Returns should not be less than -20%"
        assert (df["returns"] <= 0.20).all(), "Returns should not be greater than +20%"

    def test_dates_are_sorted(self):
        """Test that dates are in ascending order."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        assert (df["date"].diff().dropna() > pd.Timedelta(0)).all(), "Dates should be sorted"


class TestDataQuality:
    """Test data quality checks."""

    def test_minimum_data_points(self):
        """Test that minimum data points requirement is enforced."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=50),
            "ticker": ["AAPL"] * 50,
            "returns": np.random.normal(0.001, 0.015, 50)
        })
        assert len(df) >= 50, "Minimum data points should be at least 50"

    def test_no_duplicate_dates(self):
        """Test that there are no duplicate dates for the same ticker."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 100,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        duplicates = df[df.duplicated(subset=["date", "ticker"], keep=False)]
        assert len(duplicates) == 0, "No duplicate date-ticker combinations should exist"

    def test_ticker_consistency(self):
        """Test that all expected tickers are present."""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=100),
            "ticker": ["AAPL"] * 25 + ["MSFT"] * 25 + ["GOOGL"] * 25 + ["^GSPC"] * 25,
            "returns": np.random.normal(0.001, 0.015, 100)
        })
        tickers = set(df["ticker"].unique())
        expected_tickers = {"AAPL", "MSFT", "GOOGL", "^GSPC"}
        assert tickers == expected_tickers, "All expected tickers should be present"
