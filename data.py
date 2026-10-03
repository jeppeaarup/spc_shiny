import numpy as np
import pandas as pd

# Required columns for validator
REQUIRED_COLUMNS = ["value", "index"]


def validate_data_schema(data: pd.DataFrame) -> None:
    """Raise an error if data is missing any required columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        raise ValueError(f"Data is missing required columns: {missing}")


def apply_shift(values, onset, size):
    values = values.copy()
    values[onset:] += size
    return values


def apply_drift(values, onset, multiplier):
    values = values.copy()
    n = len(values) - onset
    offset = np.arange(1, n + 1) * multiplier
    values[onset:] += offset
    return values


def apply_std_increase(values, onset, multiplier, center):
    values = values.copy()
    values[onset:] = center + (values[onset:] - center) * multiplier
    return values


def simulate_data(
    n: int,
    std: float,
    mean: float,
    shift: dict | None = None,
    drift: dict | None = None,
    std_change: dict | None = None,
) -> pd.DataFrame:
    rng = np.random.default_rng()
    values = rng.normal(loc=mean, scale=std, size=n)

    true_mean = np.full(n, mean, dtype=float)
    true_std = np.full(n, std, dtype=float)

    if std_change is not None:
        values = apply_std_increase(
            values, std_change["onset"], std_change["multiplier"], center=mean
        )
        true_std = apply_std_increase(
            true_std, std_change["onset"], std_change["multiplier"], center=0
        )
    if shift is not None:
        values = apply_shift(values, shift["onset"], shift["size"])
        true_mean = apply_shift(true_mean, shift["onset"], shift["size"])
    if drift is not None:
        values = apply_drift(values, drift["onset"], drift["multiplier"])
        true_mean = apply_drift(true_mean, drift["onset"], drift["multiplier"])

    return pd.DataFrame({
        "value": values,
        "index": np.arange(n) + 1,
        "true_mean": true_mean,
        "true_std": true_std,
    })