from shiny import reactive
from shiny.express import input, ui
import data as dt
from pages.shewhart import shewhart_module

ui.page_opts(title="Control charts")

with ui.sidebar():

    # ui.card_header("Simulation controls")
    ui.input_slider("sim_n", "Number of points", 10, 200, 100)
    ui.input_slider("sim_target", "Target value", 0, 10, 0, step=0.5)
    ui.input_slider("sim_std", "Standard deviation", 1, 10, 1, step=0.1)

    ui.input_checkbox_group(
        "sim_scenarios",
        "Scenarios",
        {
            "shift": "Mean shift",
            "drift": "Drift",
            "std": "Std. deviation change",
        },
    )

    with ui.panel_conditional("input.sim_scenarios.includes('shift')"):
        ui.input_slider("shift_onset", "Shift onset", 1, 100, 50)
        ui.input_slider("shift_size", "Shift size", -10, 10, 2, step=0.1)

    with ui.panel_conditional("input.sim_scenarios.includes('drift')"):
        ui.input_slider("drift_onset", "Drift onset", 1, 100, 50)
        ui.input_slider("drift_multiplier", "Drift per point", -0.5, 0.5, 0.05, step=0.01)

    with ui.panel_conditional("input.sim_scenarios.includes('std')"):
        ui.input_slider("std_onset", "Std. onset", 1, 100, 50)
        ui.input_slider("std_multiplier", "Std. multiplier", 1, 5, 2, step=0.1)

    ui.input_action_button("sim_action", "Simulate")


@reactive.effect
def _():
    n = input.sim_n()
    for onset_id in ("shift_onset", "drift_onset", "std_onset"):
        ui.update_slider(onset_id, max=n, value=min(input[onset_id](), n))


@reactive.calc
@reactive.event(input.sim_action, ignore_none=False)
def sim_data():
    scenarios = input.sim_scenarios()

    shift = (
        {"onset": input.shift_onset() - 1, "size": input.shift_size()}
        if "shift" in scenarios else None
    )
    drift = (
        {"onset": input.drift_onset() - 1, "multiplier": input.drift_multiplier()}
        if "drift" in scenarios else None
    )
    std_change = (
        {"onset": input.std_onset() - 1, "multiplier": input.std_multiplier()}
        if "std" in scenarios else None
    )

    return dt.simulate_data(
        input.sim_n(),
        input.sim_std(),
        input.sim_target(),
        shift=shift,
        drift=drift,
        std_change=std_change,
    )


shewhart_module("shewhart", sim_data)