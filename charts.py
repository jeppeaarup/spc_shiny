import altair as alt
import numpy as np
import pandas as pd

def build_shewhart_chart(data, cal_n, limits, flags):

    PRIMARY_COLOR = "steelblue"
    ALERT_COLOR = "red"

    # Data chart
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

    line = base.mark_line(color=PRIMARY_COLOR)

    point = base.mark_point(size=100, filled=True, opacity=1).encode(
        fill=alt.Fill(
            'status',
            scale=alt.Scale(
                domain=["Calibration", "Monitoring", "Violation"],
                range=["white", PRIMARY_COLOR, ALERT_COLOR],
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

    limits_df = pd.DataFrame({
        "value": [limits.ucl, limits.lcl, limits.uwl, limits.lwl, limits.center],
        "kind": ["Control limit", "Control limit", "Warning limit", "Warning limit", "Center line"],
    })

    limit_scale = alt.Scale(
        domain=["Control limit", "Warning limit", "Center line"],
        range=[ALERT_COLOR, "orange", "black"],
    )

    limit_lines = alt.Chart(limits_df).mark_rule().encode(
        y="value:Q",
        color=alt.Color("kind:N", scale=limit_scale, legend=alt.Legend(title=None, orient='top')),
    )

    return (limit_lines + line + point
            ).configure_axis(grid=False, titleFontSize=14, labelFontSize=12
                             ).configure_legend(labelFontSize=12, symbolSize=100)


