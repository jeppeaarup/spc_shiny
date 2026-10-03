from shiny.express import ui
import pandas as pd

def violation_flag(enabled: tuple[str, ...], flags: pd.Series) -> ui.Tag:
    if not enabled:
        color, tint, symbol, text = "#6c757d", "rgba(108, 117, 125, 0.15)", "○", "No rules enabled"
    elif flags.any():
        color, tint, symbol, text = "#dc3545", "rgba(220, 53, 69, 0.12)", "⚠", "Violation detected"
    else:
        color, tint, symbol, text = "#198754", "rgba(25, 135, 84, 0.12)", "✓", "In control"

    return ui.tags.strong(
        ui.tags.span(
            symbol,
            style="display: inline-block; width: 1.4em; text-align: center;",
        ),
        text,
        style=(
            f"color: {color}; background-color: {tint}; "
            f"border: 1px solid {color}; border-radius: 4px; padding: 4px 8px; "
            "display: inline-block; max-width: 250px; text-align: left;"
        ),
    )
