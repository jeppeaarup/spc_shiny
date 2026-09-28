
# CUSUM card ----
with ui.nav_panel("CUSUM"):
    with ui.layout_sidebar():
        with ui.sidebar(position="right"):
            ui.input_slider("cusum_k", "Slack (k)", 0.1, 1.5, 0.5, step=0.1)
            ui.input_slider("cusum_h", "Decision interval (h)", 0.0, 8.0, 1, step=0.1)

            ui.input_slider("cusum_cp", "Current point", 1, 100, 100, step=1)

            @reactive.effect
            def _():
                n = len(sim_data())
                current = input.cal_n()
                ui.update_slider("cusum_cp", max=n, value=min(current, n))

        @render_altair
        def cusum_chart():
            flags = shewhart_violations()
            return cu.build_chart(sim_data(), input.cal_n(), flags, input.cusum_cp(), input.cusum_h(), input.cusum_k(), dist=20)
