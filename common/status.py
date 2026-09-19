def get_violation_status(enabled: bool, flags: pd.Series) -> tuple[str, str]:
    """
    Determine the status color/text for a violation indicator.

    enabled: whether any detection rule/check is currently active.
    flags: boolean Series of per-point violation flags.
    """
    if not enabled:
        return "grey", "No rules enabled"
    elif flags.any():
        return "red", "⚠ Violation detected"
    else:
        return "green", "✓ In control"