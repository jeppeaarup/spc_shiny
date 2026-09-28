import altair as alt
import pandas as pd
from common import build_base_chart

def build_chart(data: pd.DataFrame, cal_n: int, flags: pd.Series, cpx: int, h: float, k: float, dist: float) -> alt.LayerChart:
    """Build the full CUSUM chart: base line/points plus the V-mask."""

    base = build_base_chart(data, cal_n, flags)

    cpy = data.iloc[cpx - 1].value  # Current point y
    bpx = cpx - dist                # Back point x
    bph = h + k * dist              # Back point height (offset from y)

    vmask_df = pd.DataFrame([
        {'arm': 'vertical', 'x': cpx, 'y': cpy - h},
        {'arm': 'vertical', 'x': cpx, 'y': cpy + h},
        {'arm': 'upper', 'x': cpx, 'y': cpy + h},
        {'arm': 'upper', 'x': bpx, 'y': cpy + bph},
        {'arm': 'lower', 'x': cpx, 'y': cpy - h},
        {'arm': 'lower', 'x': bpx, 'y': cpy - bph},
    ])

    vmask_lines = alt.Chart(vmask_df).mark_line(color='red').encode(
        x='x:Q',
        y='y:Q',
        detail='arm:N',
    )

    return (vmask_lines + base).configure_axis(grid=False, titleFontSize=20, labelFontSize=20)