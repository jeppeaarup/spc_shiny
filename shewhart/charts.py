import altair as alt
import pandas as pd
from common import build_base_chart
from shewhart.limits import ShewhartLimits

def build_chart(data: pd.DataFrame, cal_n: int, limits: ShewhartLimits, flags: pd.Series) -> alt.LayerChart:
    """Build the full Shewhart chart: base line/points plus control and warning limit lines."""

    base = build_base_chart(data, cal_n, flags)

    limits_df = pd.DataFrame({
        "value": [limits.ucl, limits.lcl, limits.uwl, limits.lwl, limits.center],
        "kind": ["Control limit", "Control limit", "Warning limit", "Warning limit", "Center line"],
    })

    limit_scale = alt.Scale(
        domain=["Control limit", "Warning limit", "Center line"],
        range=["red", "orange", "black"],
    )

    limit_lines = alt.Chart(limits_df).mark_rule().encode(
        y="value:Q",
        color=alt.Color("kind:N", scale=limit_scale, legend=alt.Legend(title=None, orient='top')),
    )

    return (limit_lines + base
            ).configure_axis(
                grid=False, titleFontSize=14, labelFontSize=12
                ).configure_legend(labelFontSize=12, symbolSize=100)