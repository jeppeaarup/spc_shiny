import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["value", "index"]

def simulate_data(n: int, std: float, mean: float) -> pd.DataFrame:
    """Simulate n normally-distributed process values around mean, with the given std."""
    rng = np.random.default_rng()
    data = pd.DataFrame({
        'value': rng.normal(loc=mean, scale=std, size=n),
        'index': np.arange(n) + 1
    })
    return data

def validate_data_schema(data: pd.DataFrame) -> None:
    """Raise an error if data is missing any required columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        raise ValueError(f"Data is missing required columns: {missing}")