import numpy as np
import pandas as pd
from scipy.optimize import minimize
import os

from src.utils.config import FEATURE_DIR, TICKERS
from src.utils.helpers import align_dataframes_on_date


# ----------------------------
# LOAD + ALIGN RETURNS
# ----------------------------

def get_aligned_returns():
    dfs = []

    for ticker in TICKERS:
        path = os.path.join(FEATURE_DIR, f"{ticker}.parquet")

        if not os.path.exists(path):
            raise FileNotFoundError(f"{ticker} feature file not found")

        df = pd.read_parquet(path)

        # Ensure required columns
        if "date" not in df.columns or "returns" not in df.columns:
            raise ValueError(f"{ticker} missing required columns")

        # Select and rename safely (no rename() issue)
        df = df[["date", "returns"]].copy()
        df.columns = ["date", ticker]

        dfs.append(df)

    aligned = align_dataframes_on_date(dfs)

    # Final safety check
    if aligned.isna().sum().sum() > 0:
        raise ValueError("NaNs detected after alignment")

    if len(aligned) < 50:
        raise ValueError("Not enough data after alignment")

    return aligned


# ----------------------------
# PORTFOLIO METRICS
# ----------------------------

def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(weights.T @ cov_matrix @ weights)


def portfolio_return(weights, mean_returns):
    return np.sum(weights * mean_returns)


# ----------------------------
# OPTIMIZATION
# ----------------------------

def optimize_portfolio():
    returns_df = get_aligned_returns()

    mean_returns = returns_df.mean().values
    cov_matrix = returns_df.cov().values

    # Covariance stability check
    if np.linalg.det(cov_matrix) == 0:
        raise ValueError("Covariance matrix is singular")

    n = len(TICKERS)
    init_weights = np.ones(n) / n

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n

    result = minimize(
        portfolio_volatility,
        init_weights,
        args=(cov_matrix,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    return result.x, mean_returns, cov_matrix


# ----------------------------
# MAIN (EXECUTION + VERIFICATION)
# ----------------------------

if __name__ == "__main__":
    weights, mean_returns, cov_matrix = optimize_portfolio()

    print("\nOptimal Portfolio Weights:")
    for ticker, weight in zip(TICKERS, weights):
        print(f"{ticker}: {weight:.4f}")

    print(f"\nSum of weights: {np.sum(weights):.4f}")

    print("\nPortfolio Expected Return:")
    print(np.sum(weights * mean_returns))

    print("\nPortfolio Volatility:")
    print(portfolio_volatility(weights, cov_matrix))