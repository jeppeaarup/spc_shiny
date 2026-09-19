from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_altair
import pandas as pd

import data as dt
import common as cm
import shewhart as sh

with ui.sidebar():
    with ui.card():
        ui.card_header("Simulation controls")
        ui.input_slider("sim_n", "Number of data points", 0, 200, 100)
        ui.input_slider("sim_mean", "Mean", 0, 10, 0, step=0.5)
        ui.input_slider("sim_std", "Standard deviation", 1, 10, 1, step=0.1)
        ui.input_action_button("sim_action", "Simulate")

    with ui.card():
        ui.card_header("Calibration controls")
        
        @render.table(header=False, border=1)
        def cal_stats_display():
            stats = cal_stats()
            return pd.DataFrame({
                "Statistic": ["Mean", "Std. dev."],
                "Value": [round(stats.mean, 2), round(stats.std, 2)]
            })

        ui.input_slider("cal_n", "Calibration points", 2, 200, 50)
        @reactive.effect
        def _():
            n = len(sim_data())
            current = input.cal_n()
            ui.update_slider("cal_n", max=n, value=min(current, n))

@reactive.calc
@reactive.event(input.sim_action, ignore_none=False)
def sim_data():
    return dt.simulate_data(input.sim_n(), input.sim_std(), input.sim_mean())

@reactive.calc
def cal_stats():
    return cm.compute_calibration_stats(sim_data(), input.cal_n())

@reactive.calc
def shewhart_limits():
    return sh.compute_limits(
        cal_stats(),
        k_warning=input.shewhart_warning_k(),
        k_control=input.shewhart_control_k(),
    )

@reactive.calc
def shewhart_violations():
    return sh.compute_violations(
        sim_data(), 
        input.cal_n(), 
        shewhart_limits(), 
        input.shewhart_enabled_rules()
    )

# Shewhart chart card ----
with ui.card():
    ui.card_header("Shewhart chart")
    with ui.layout_sidebar():
        with ui.sidebar(position="right"):
            @render.express
            def violation_status():
                color, text = cm.get_violation_status(bool(input.shewhart_enabled_rules()), shewhart_violations())
                ui.tags.strong(
                    text,
                    style=f"color: {color}; border: 1px solid {color}; padding: 4px 8px; border-radius: 4px;"
                )

            ui.input_slider("shewhart_warning_k", "Warning limit k", 0, 10, 2, step=0.1)
            ui.input_slider("shewhart_control_k", "Control limit k", 0, 10, 3, step=0.1)

            ui.input_checkbox_group("shewhart_enabled_rules", "Enabled rules",
                                    {
                                        "beyond_limit": "Outside CL",
                                        "two_in_a_row": "2 in a row outside WL",
                                        "trend": "7 in a row increasing or decreasing",
                                        "bias": "8 in a row on same side of center"
                                     })
        @render_altair
        def shewhart_chart():
            flags = shewhart_violations()
            return sh.build_chart(sim_data(), input.cal_n(), shewhart_limits(), flags)

# CUSUM card ----
with ui.card():
    ui.card_header("CUSUM Chart")
    with ui.layout_sidebar():
        with ui.sidebar(position="right"):
            ui.input_slider("k", "Slack (k)", 0.1, 1.5, 0.5, step=0.05)
            ui.input_slider("h", "Decision interval (h)", 2.0, 8.0, 5.0, step=0.5)