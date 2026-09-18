from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class CalibrationStats:
    """Sample stats computed on calibration points."""
    mean: float
    std: float

@dataclass
class ShewhartLimits:
    """Center line and control/warning limits for a Shewhart chart."""
    center: float
    ucl: float
    lcl: float
    uwl: float
    lwl: float

def compute_calibration_stats(data, n_cal):
    calibration_data = data.iloc[:n_cal]
    return CalibrationStats(
        mean=np.mean(calibration_data['value']),
        std=np.std(calibration_data['value'], ddof=1)
    )

def compute_shewhart_limits(cal_stats, k_warning=2, k_control=3):
    std = cal_stats.std
    mean = cal_stats.mean
    control_spacer = k_control * std
    warning_spacer = k_warning * std
    return ShewhartLimits(
        center=mean,
        ucl=mean + control_spacer,
        lcl=mean - control_spacer,
        uwl=mean + warning_spacer,
        lwl=mean - warning_spacer
    )


def rule_beyond_limit(values, limits):
    """Flag points beyond the control limits."""
    values = pd.Series(values)
    return (values > limits.ucl) | (values < limits.lcl)

def rule_two_in_a_row(values, limits):
    """Flag the second of two consecutive points beyond the warning limit, same side."""
    values = pd.Series(values)
    above = values > limits.uwl
    below = values < limits.lwl
    two_above = above & above.shift(1, fill_value=False)
    two_below = below & below.shift(1, fill_value=False)
    return two_above | two_below


def rule_trend(values, window=7):
    """Flag the last point of `window` consecutive monotonically increasing or decreasing points."""
    values = pd.Series(values)
    diffs = values.diff()
    increasing = (diffs > 0).rolling(window - 1).sum() == (window - 1)
    decreasing = (diffs < 0).rolling(window - 1).sum() == (window - 1)
    return (increasing | decreasing).fillna(False)


def rule_bias(values, limits, window=8):
    """Flag the last point of `window` consecutive points on the same side of center."""
    values = pd.Series(values)
    above = values > limits.center
    below = values < limits.center
    all_above = above.rolling(window).sum() == window
    all_below = below.rolling(window).sum() == window
    return (all_above | all_below).fillna(False)


def compute_shewhart_violations(data, cal_n, limits, enabled_rules=None):
    """Flag Shewhart rule violations on monitoring points."""
    if enabled_rules is None:
        enabled_rules = []

    values = data["value"].iloc[cal_n:]
    flags = pd.Series(False, index=data.index)

    if "beyond_limit" in enabled_rules:
        flags.loc[values.index] |= rule_beyond_limit(values, limits)
    if "two_in_a_row" in enabled_rules:
        flags.loc[values.index] |= rule_two_in_a_row(values, limits)
    if "trend" in enabled_rules:
        flags.loc[values.index] |= rule_trend(values)
    if "bias" in enabled_rules:
        flags.loc[values.index] |= rule_bias(values, limits)

    return flags