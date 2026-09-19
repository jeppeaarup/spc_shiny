import pandas as pd
from shewhart.limits import ShewhartLimits

def _rule_beyond_limit(values: pd.Series, limits: ShewhartLimits) -> pd.Series:
    """Flag points beyond the control limits."""
    return (values > limits.ucl) | (values < limits.lcl)


def _rule_two_in_a_row(values: pd.Series, limits: ShewhartLimits) -> pd.Series:
    """Flag the second of two consecutive points beyond the warning limit, same side."""
    above = values > limits.uwl
    below = values < limits.lwl
    two_above = above & above.shift(1, fill_value=False)
    two_below = below & below.shift(1, fill_value=False)
    return two_above | two_below


def _rule_trend(values: pd.Series, window: int = 7) -> pd.Series:
    """Flag the last point of `window` consecutive monotonically increasing or decreasing points."""
    diffs = values.diff()
    increasing = (diffs > 0).rolling(window - 1).sum() == (window - 1)
    decreasing = (diffs < 0).rolling(window - 1).sum() == (window - 1)
    return (increasing | decreasing).fillna(False)


def _rule_bias(values: pd.Series, limits: ShewhartLimits, window: int = 8) -> pd.Series:
    """Flag the last point of `window` consecutive points on the same side of center."""
    above = values > limits.center
    below = values < limits.center
    all_above = above.rolling(window).sum() == window
    all_below = below.rolling(window).sum() == window
    return (all_above | all_below).fillna(False)


def compute_violations(data: pd.DataFrame, cal_n: int, limits: ShewhartLimits, enabled_rules: list[str] | None = None) -> pd.Series:
    """Flag Shewhart rule violations on monitoring points."""
    if enabled_rules is None:
        enabled_rules = []

    values = data["value"].iloc[cal_n:]
    flags = pd.Series(False, index=data.index)

    if "beyond_limit" in enabled_rules:
        flags.loc[values.index] |= _rule_beyond_limit(values, limits)
    if "two_in_a_row" in enabled_rules:
        flags.loc[values.index] |= _rule_two_in_a_row(values, limits)
    if "trend" in enabled_rules:
        flags.loc[values.index] |= _rule_trend(values)
    if "bias" in enabled_rules:
        flags.loc[values.index] |= _rule_bias(values, limits)

    return flags