import numpy as np
import pandas as pd


def apply_shift(values, onset, size):
    2+2

def simulate_data(n, std, mean):
    rng = np.random.default_rng()
    return pd.DataFrame({
        'value': rng.normal(loc=mean, scale=std, size=n),
        'index': np.arange(n) + 1
    })

