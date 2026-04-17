import pandas as pd

# Load returns
df = pd.read_parquet("data/marts/fact_returns.parquet")

# Pivot to wide format
pivot = df.pivot(index="date", columns="ticker", values="returns")

# Fill missing
pivot = pivot.fillna(0)

# Compute cumulative returns
cum_returns = (1 + pivot).cumprod()

# Compute rolling max
rolling_max = cum_returns.cummax()

# Compute drawdown
drawdown = (cum_returns - rolling_max) / rolling_max

# Convert to long format (Tableau-friendly)
drawdown_long = drawdown.stack().reset_index()
drawdown_long.columns = ["date", "ticker", "drawdown"]

# Save
drawdown_long.to_csv("data/marts/drawdown.csv", index=False)