import reflex as rx

from .history_state import HistoryState
from .nav_bar import nav_bar


def _section(icon: str, title: str, headers: list[str], rows: rx.Var, row_keys: list[str]) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=20, color="var(--violet-9)"),
            rx.heading(title, size="4"),
            spacing="2",
            align="center",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(*[rx.table.column_header_cell(h) for h in headers]),
            ),
            rx.table.body(
                rx.foreach(
                    rows,
                    lambda item: rx.table.row(
                        *[rx.table.cell(item[key]) for key in row_keys],
                    ),
                ),
            ),
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding="1.5em",
        background="var(--color-panel-solid)",
        border="1px solid var(--gray-6)",
        border_radius="var(--radius-4)",
        align="start",
    )


def history() -> rx.Component:
    return rx.vstack(
        nav_bar(),
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.icon("history", size=28, color="var(--violet-9)"),
                    rx.heading("History", size="7", color_scheme="violet"),
                    spacing="2",
                    align="center",
                ),
                _section(
                    "dumbbell",
                    "Workout History",
                    ["Date", "Workout Type", "Duration"],
                    HistoryState.workout_history,
                    ["date", "workout_type", "duration"],
                ),
                _section(
                    "scale",
                    "Weight History",
                    ["Date", "Weight", "Change"],
                    HistoryState.weight_history,
                    ["date", "weight", "change"],
                ),
                _section(
                    "flame",
                    "Calories History",
                    ["Date", "Consumed (kcal)", "Burned (kcal)"],
                    HistoryState.calorie_history,
                    ["date", "consumed", "burned"],
                ),
                _section(
                    "footprints",
                    "Steps History",
                    ["Date", "Steps", "Daily Goal"],
                    HistoryState.step_history,
                    ["date", "steps", "daily_goal"],
                ),
                spacing="5",
                width="50em",
                max_width="95vw",
                padding="2em",
            ),
            width="100%",
        ),
        width="100%",
        spacing="0",
        align="center",
        min_height="100vh",
        background="linear-gradient(135deg, var(--blue-3), var(--purple-3))",
    )
