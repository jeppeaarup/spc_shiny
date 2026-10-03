from shiny.express import ui

def section_header(text: str) -> ui.Tag:
    return ui.tags.div(
        text,
        style=(
            "font-size: 14px; line-height: 1.5; font-weight: 700; "
            "text-transform: uppercase; letter-spacing: 0.05em; "
            "color: var(--bs-primary); "
            "border-bottom: 1px solid var(--bs-border-color); "
            "padding-left: 0px; padding-bottom: 4px; "
            "margin-top: 1.25rem; margin-bottom: 0.1rem;"
        )
    )

def stat_tile(label: str, value: float, decimals: int = 2) -> ui.Tag:
    return ui.tags.div(
        ui.tags.div(label, style="font-size: 0.8rem; color: grey;"),
        ui.tags.div(f"{value:.{decimals}f}", style="font-size: 1.1rem; font-weight: 600;"),
        style="text-align: center; border: 1px solid #ddd; border-radius: 4px; padding: 4px 2px; min-width: 0; overflow: hidden; box-sizing: border-box;",
    )