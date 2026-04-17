import pandas as pd

# Load returns
df = pd.read_parquet("data/marts/fact_returns.parquet")

# Pivot: rows = date, columns = ticker
pivot = df.pivot(index="date", columns="ticker", values="returns")

# Compute correlation matrix
corr = pivot.corr()

# Set index and column names to avoid conflicts when stacking
corr.index.name = "ticker_1"
corr.columns.name = "ticker_2"

# Convert to long format (Tableau-friendly)
corr_long = corr.stack().reset_index()
corr_long.columns = ["ticker_1", "ticker_2", "correlation"]

# Save
corr_long.to_csv("data/marts/correlation_matrix.csv", index=False)