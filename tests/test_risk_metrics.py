"""Tests for risk metrics calculation module."""

import pytest
import numpy as np
import pandas as pd
from src.quant.risk_metrics import sharpe_ratio, max_drawdown


class TestSharpeRatio:
    """Test sharpe_ratio function."""

    def test_sharpe_ratio_positive_returns(self):
        """Test Sharpe ratio with positive returns."""
        returns = pd.Series([0.01, 0.015, 0.02, 0.012, 0.018] * 50)
        sr = sharpe_ratio(returns)
        assert sr > 0, "Sharpe ratio should be positive for positive returns"

    def test_sharpe_ratio_negative_returns(self):
        """Test Sharpe ratio with negative returns."""
        returns = pd.Series([-0.01, -0.015, -0.02, -0.012, -0.018] * 50)
        sr = sharpe_ratio(returns)
        assert sr < 0, "Sharpe ratio should be negative for negative returns"

    def test_sharpe_ratio_zero_volatility(self):
        """Test Sharpe ratio with zero volatility (constant returns)."""
        returns = pd.Series([0.001] * 252)
        sr = sharpe_ratio(returns)
        assert np.isfinite(sr), "Sharpe ratio should be finite"

    def test_sharpe_ratio_returns_numeric(self):
        """Test that Sharpe ratio returns a numeric value."""
        returns = pd.Series(np.random.normal(0.001, 0.015, 252))
        sr = sharpe_ratio(returns)
        assert isinstance(sr, (float, np.floating)), "Sharpe ratio should be numeric"


class TestMaxDrawdown:
    """Test max_drawdown function."""

    def test_max_drawdown_positive_returns(self):
        """Test max drawdown with all positive returns (no drawdown)."""
        returns = pd.Series([0.01] * 100)
        mdd = max_drawdown(returns)
        assert mdd == 0, "Max drawdown should be 0 for all positive returns"

    def test_max_drawdown_negative_returns(self):
        """Test max drawdown with negative returns."""
        returns = pd.Series([-0.10, -0.05, 0.02] * 30)
        mdd = max_drawdown(returns)
        assert mdd < 0, "Max drawdown should be negative"
        assert mdd >= -1, "Max drawdown should not exceed -100%"

    def test_max_drawdown_single_drop(self):
        """Test max drawdown with a single significant drop."""
        returns = pd.Series([0.05] * 50 + [-0.30] + [0.02] * 50)
        mdd = max_drawdown(returns)
        assert mdd < -0.2, "Max drawdown should capture the significant drop"

    def test_max_drawdown_returns_numeric(self):
        """Test that max drawdown returns a numeric value."""
        returns = pd.Series(np.random.normal(0.001, 0.015, 252))
        mdd = max_drawdown(returns)
        assert isinstance(mdd, (float, np.floating)), "Max drawdown should be numeric"

    def test_max_drawdown_range(self):
        """Test that max drawdown is between -1 and 0."""
        returns = pd.Series(np.random.normal(0.001, 0.02, 252))
        mdd = max_drawdown(returns)
        assert -1 <= mdd <= 0, "Max drawdown should be between -1 and 0"
