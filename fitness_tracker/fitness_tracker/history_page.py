import reflex as rx

from .history_state import HistoryState


def _section(title: str, headers: list[str], rows: rx.Var, row_keys: list[str]) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="4"),
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
        border="1px solid var(--gray-6)",
        border_radius="var(--radius-4)",
        align="start",
    )


def history() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("History", size="7", color_scheme="blue"),
                rx.spacer(),
                rx.link("Back to Home", href="/home", color_scheme="blue"),
                width="100%",
                align="center",
            ),
            _section(
                "Workout History",
                ["Date", "Workout Type", "Duration"],
                HistoryState.workout_history,
                ["date", "workout_type", "duration"],
            ),
            _section(
                "Weight History",
                ["Date", "Weight", "Change"],
                HistoryState.weight_history,
                ["date", "weight", "change"],
            ),
            _section(
                "Calories History",
                ["Date", "Consumed (kcal)", "Burned (kcal)"],
                HistoryState.calorie_history,
                ["date", "consumed", "burned"],
            ),
            _section(
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
    )
