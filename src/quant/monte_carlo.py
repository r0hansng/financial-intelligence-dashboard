import numpy as np
import pandas as pd
import os

from src.utils.config import FEATURE_DIR

def simulate(ticker, days=252, sims=1000):
    df = pd.read_parquet(os.path.join(FEATURE_DIR, f"{ticker}.parquet"))

    mu = df["returns"].mean()
    sigma = df["returns"].std()

    simulations = []

    for _ in range(sims):
        prices = [1]
        for _ in range(days):
            shock = np.random.normal(mu, sigma)
            prices.append(prices[-1] * (1 + shock))
        simulations.append(prices)

    return np.array(simulations)

if __name__ == "__main__":
    sim = simulate("AAPL")
    print(sim.shape)