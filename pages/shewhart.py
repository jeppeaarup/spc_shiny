from shiny import reactive
from shiny.express import module, render, ui
from shinywidgets import render_altair

import common as cm
import shewhart as sh

@module
def shewhart_module(input, output, session, sim_data):
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
            input.shewhart_enabled_rules(),
        )

    with ui.nav_panel("Shewhart"):
        with ui.layout_sidebar():
            with ui.sidebar(position="right", width="20%"):
                @render.express
                def violation_status():
                    cm.violation_flag(
                        enabled=input.shewhart_enabled_rules(),
                        flags=shewhart_violations(),
                    )
                    
                cm.section_header("Calibration controls")

                @render.express
                def cal_stats_text():
                    stats = cal_stats()
                    with ui.layout_column_wrap(width="80px", fill=False):
                        cm.stat_tile("Mean", stats.mean)
                        cm.stat_tile("Std. dev.", stats.std)

                ui.input_slider("cal_n", "Calibration points", 2, 200, 50)
                ui.input_slider("shewhart_warning_k", "Warning limit (k)", 0, 10, 2, step=0.1)
                ui.input_slider("shewhart_control_k", "Control limit (k)", 0, 10, 3, step=0.1)

                @reactive.effect
                def _():
                    n = len(sim_data())
                    current = input.cal_n()
                    ui.update_slider("cal_n", max=n, value=min(current, n))

                cm.section_header("Enabled rules")
                ui.input_checkbox_group(
                    "shewhart_enabled_rules",
                    "",
                    {
                        "beyond_limit": "Outside CL",
                        "two_in_a_row": "2 in a row outside WL",
                        "trend": "7 in a row increasing or decreasing",
                        "bias": "8 in a row on same side of center",
                    },
                    selected="beyond_limit",
                )

            with ui.card():
                ui.card_header("Shewhart chart")

                @render_altair
                def shewhart_chart():
                    flags = shewhart_violations()
                    return sh.build_chart(sim_data(), input.cal_n(), shewhart_limits(), flags)
            with ui.card():
                ui.card_header("SPC Theory")
                ui.markdown("""
                ## What is a control chart?

                $$
                x_i \\sim N(\\mu,\\sigma)
                $$

                A control chart plots a process variable over time, with...
                """)