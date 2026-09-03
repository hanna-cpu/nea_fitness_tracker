import reflex as rx

from .app_state import State
from .home_state import HomeState
from .nav_bar import nav_bar


def _card(*children: rx.Component, **props) -> rx.Component:
    props.setdefault("align", "start")
    return rx.vstack(
        *children,
        spacing="3",
        width="100%",
        padding="1.5em",
        background="var(--color-panel-solid)",
        border="1px solid var(--gray-6)",
        border_radius="var(--radius-4)",
        **props,
    )


def _notification_banner(notification: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.icon("bell", size=18, color="var(--amber-9)"),
        rx.text(notification["message"], size="3"),
        rx.spacer(),
        rx.icon_button(
            rx.icon("x", size=14),
            on_click=State.dismiss_notification(notification["id"]),
            variant="ghost",
            color_scheme="gray",
            size="1",
        ),
        width="100%",
        padding="0.75em 1em",
        background="var(--amber-3)",
        border="1px solid var(--amber-6)",
        border_radius="var(--radius-3)",
        align="center",
    )


def _steps_card() -> rx.Component:
    return _card(
        rx.hstack(
            rx.icon("footprints", size=22, color="var(--blue-9)"),
            rx.heading("Daily Steps", size="4"),
            spacing="2",
            align="center",
        ),
        rx.text(f"{HomeState.steps_current} / {HomeState.steps_target} steps today", size="3", color="gray"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="steps", fill="var(--blue-9)", radius=[6, 6, 0, 0]),
            rx.recharts.x_axis(data_key="date"),
            rx.recharts.y_axis(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.tooltip(),
            rx.recharts.reference_line(y=HomeState.steps_target.to(int), stroke="var(--red-9)", label="Goal"),
            data=HomeState.steps_series,
            height=220,
        ),
    )


def _workout_card() -> rx.Component:
    return _card(
        rx.hstack(
            rx.icon("dumbbell", size=22, color="var(--indigo-9)"),
            rx.heading("Workout Duration", size="4"),
            spacing="2",
            align="center",
        ),
        rx.text(f"{HomeState.workout_current} / {HomeState.workout_target} min today", size="3", color="gray"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="minutes", fill="var(--indigo-9)", radius=[6, 6, 0, 0]),
            rx.recharts.x_axis(data_key="date"),
            rx.recharts.y_axis(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.tooltip(),
            rx.recharts.reference_line(y=HomeState.workout_target.to(int), stroke="var(--red-9)", label="Goal"),
            data=HomeState.workout_series,
            height=220,
        ),
    )


def _weight_card() -> rx.Component:
    return _card(
        rx.hstack(
            rx.icon("scale", size=22, color="var(--violet-9)"),
            rx.heading("Weight Trend", size="4"),
            spacing="2",
            align="center",
        ),
        rx.text(f"{HomeState.weight_current} kg (goal {HomeState.weight_target} kg)", size="3", color="gray"),
        rx.recharts.line_chart(
            rx.recharts.line(data_key="weight", stroke="var(--violet-9)", type_="monotone", dot=True),
            rx.recharts.x_axis(data_key="date"),
            rx.recharts.y_axis(domain=["auto", "auto"]),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.tooltip(),
            rx.recharts.reference_line(y=HomeState.weight_target.to(int), stroke="var(--red-9)", label="Goal"),
            data=HomeState.weight_series,
            height=220,
        ),
    )


def _calories_card() -> rx.Component:
    return _card(
        rx.hstack(
            rx.icon("flame", size=22, color="var(--purple-9)"),
            rx.heading("Calories", size="4"),
            spacing="2",
            align="center",
        ),
        rx.text(f"{HomeState.calories_current} / {HomeState.calories_target} kcal burned today", size="3", color="gray"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="consumed", fill="var(--purple-6)", name="Consumed", radius=[6, 6, 0, 0]),
            rx.recharts.bar(data_key="burned", fill="var(--purple-9)", name="Burned", radius=[6, 6, 0, 0]),
            rx.recharts.x_axis(data_key="date"),
            rx.recharts.y_axis(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            data=HomeState.calories_series,
            height=220,
        ),
    )


def home() -> rx.Component:
    return rx.vstack(
        nav_bar(),
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.icon("activity", size=28, color="var(--violet-9)"),
                    rx.heading("Welcome back", size="7", color_scheme="violet"),
                    spacing="2",
                    align="center",
                ),
                rx.text(State.username, size="5", weight="bold"),
                rx.vstack(
                    rx.foreach(State.notifications, _notification_banner),
                    width="100%",
                    spacing="2",
                ),
                rx.grid(
                    _steps_card(),
                    _workout_card(),
                    _weight_card(),
                    _calories_card(),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                spacing="6",
                width="60em",
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
