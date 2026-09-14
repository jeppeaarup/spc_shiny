from shiny import reactive
from shiny.express import input, ui
from shinywidgets import render_altair
from simulation import *

ui.input_slider("slider", "Slider", 0, 100, 50)
ui.input_action_button("go", "Run")

@render_altair
@reactive.event(input.go)
def hist():
    import altair as alt
    df = simulate_data(input.slider())
    return (
        alt.Chart(df)
        .mark_point()
        .encode(x='x', y='y')
    )