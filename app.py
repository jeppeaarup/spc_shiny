from shiny import reactive
from shiny.express import input, ui

import data as dt

from pages.shewhart import shewhart_module

ui.page_opts(title="Control charts")

with ui.sidebar():
    with ui.card():
        ui.card_header("Simulation controls")
        ui.input_slider("sim_n", "Number of points", 10, 200, 100)
        ui.input_slider("sim_mean", "Target value", 0, 10, 0, step=0.5)
        ui.input_slider("sim_std", "Standard deviation", 1, 10, 1, step=0.1)
        ui.input_action_button("sim_action", "Simulate")


@reactive.calc
@reactive.event(input.sim_action, ignore_none=False)
def sim_data():
    return dt.simulate_data(input.sim_n(), input.sim_std(), input.sim_mean())


shewhart_module("shewhart", sim_data)