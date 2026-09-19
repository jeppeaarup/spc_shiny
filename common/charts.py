import altair as alt
import numpy as np
import pandas as pd

PRIMARY_COLOR = "steelblue"
CALIBRATION_FILL = "white"
ALERT_COLOR = "red"


def build_base_chart(data: pd.DataFrame, cal_n: int, flags: pd.Series) -> alt.LayerChart:
    """
    Build the shared line + point layer used by all control charts.
    """
    
    # Add data columns
    data = data.copy()
    data["period"] = np.where(data["index"] <= cal_n, "Calibration", "Monitoring")
    data["flagged"] = flags
    data["status"] = np.select(
        condlist=[data["flagged"], data["period"] == "Calibration"],
        choicelist=["Violation", "Calibration"],
        default="Monitoring",
    )

    # Base chart
    base = alt.Chart(data).encode(
        x=alt.X('index:Q').title('Index'),
        y=alt.Y('value:Q', scale=alt.Scale(padding=20)).title('Value'),
    )

    # Data chart
    line = base.mark_line(color=PRIMARY_COLOR)

    point = base.mark_point(size=100, filled=True, opacity=1).encode(
        fill=alt.Fill(
            'status',
            scale=alt.Scale(
                domain=["Calibration", "Monitoring", "Violation"],
                range=[CALIBRATION_FILL, PRIMARY_COLOR, ALERT_COLOR],
            ),
            legend=alt.Legend(title=None, orient='top'),
        ),
        stroke=alt.Stroke(
            'status',
            scale=alt.Scale(
                domain=["Calibration", "Monitoring", "Violation"],
                range=[PRIMARY_COLOR, PRIMARY_COLOR, ALERT_COLOR],
            ),
            legend=None,
        ),
    )

    return line + point