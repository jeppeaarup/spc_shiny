from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class CalibrationStats:
    """Sample stats computed on calibration points."""
    mean: float
    std: float


def compute_calibration_stats(data: pd.DataFrame, n_cal: int) -> CalibrationStats:
    """Compute sample mean/std over the first n_cal rows of data."""
    calibration_data = data.iloc[:n_cal]
    return CalibrationStats(
        mean=np.mean(calibration_data['value']),
        std=np.std(calibration_data['value'], ddof=1)
    )