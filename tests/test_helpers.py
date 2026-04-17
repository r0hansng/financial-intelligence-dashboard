"""Tests for utility helper functions."""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from src.utils.helpers import (
    ensure_datetime,
    sort_by_date,
    align_dataframes_on_date
)


class TestDateTimeUtilities:
    """Test date/time utility functions."""

    def test_ensure_datetime_valid_dates(self):
        """Test that ensure_datetime handles valid dates."""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02", "2020-01-03"],
            "value": [1, 2, 3]
        })
        result = ensure_datetime(df)
        assert pd.api.types.is_datetime64_any_dtype(result["date"]), "Date column should be datetime"

    def test_ensure_datetime_raises_on_invalid_dates(self):
        """Test that ensure_datetime raises error on invalid dates."""
        df = pd.DataFrame({
            "date": ["2020-01-01", "invalid-date", "2020-01-03"],
            "value": [1, 2, 3]
        })
        with pytest.raises(ValueError):
            ensure_datetime(df)

    def test_sort_by_date_ascending(self):
        """Test that sort_by_date sorts in ascending order."""
        df = pd.DataFrame({
            "date": pd.to_datetime(["2020-01-03", "2020-01-01", "2020-01-02"]),
            "value": [3, 1, 2]
        })
        result = sort_by_date(df)
        assert (result["date"].iloc[0] < result["date"].iloc[1] < result["date"].iloc[2]), \
            "Dates should be sorted in ascending order"

    def test_sort_by_date_preserves_data(self):
        """Test that sort_by_date preserves data integrity."""
        df = pd.DataFrame({
            "date": pd.to_datetime(["2020-01-03", "2020-01-01", "2020-01-02"]),
            "value": [3, 1, 2]
        })
        result = sort_by_date(df)
        assert len(result) == len(df), "Sort should preserve row count"
        assert set(result["value"]) == {1, 2, 3}, "Sort should preserve values"


class TestDataFrameAlignment:
    """Test DataFrame alignment functions."""

    def test_align_dataframes_common_dates(self):
        """Test alignment of DataFrames with common dates."""
        df1 = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "AAPL": np.random.normal(0.001, 0.015, 5)
        })
        df2 = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "MSFT": np.random.normal(0.001, 0.015, 5)
        })
        result = align_dataframes_on_date([df1, df2])
        assert len(result) == 5, "Aligned DataFrame should have 5 rows"
        assert "AAPL" in result.columns and "MSFT" in result.columns, \
            "Aligned DataFrame should have both columns"

    def test_align_dataframes_partial_overlap(self):
        """Test alignment of DataFrames with partial date overlap."""
        df1 = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "AAPL": np.random.normal(0.001, 0.015, 5)
        })
        df2 = pd.DataFrame({
            "date": pd.date_range("2020-01-03", periods=5),
            "MSFT": np.random.normal(0.001, 0.015, 5)
        })
        result = align_dataframes_on_date([df1, df2])
        # Should have only overlapping dates (3 days)
        assert len(result) == 3, "Aligned DataFrame should have 3 rows (common dates)"

    def test_align_dataframes_no_missing_values(self):
        """Test that aligned DataFrame has no missing values."""
        df1 = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "AAPL": np.random.normal(0.001, 0.015, 10)
        })
        df2 = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "MSFT": np.random.normal(0.001, 0.015, 10)
        })
        result = align_dataframes_on_date([df1, df2])
        assert result.isnull().sum().sum() == 0, "Aligned DataFrame should have no missing values"

    def test_align_dataframes_multiple_dfs(self):
        """Test alignment of multiple DataFrames."""
        dfs = []
        for ticker in ["AAPL", "MSFT", "GOOGL"]:
            df = pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=10),
                ticker: np.random.normal(0.001, 0.015, 10)
            })
            dfs.append(df)
        result = align_dataframes_on_date(dfs)
        assert len(result) == 10, "Aligned DataFrame should have 10 rows"
        assert len(result.columns) == 3, "Aligned DataFrame should have 3 columns"
