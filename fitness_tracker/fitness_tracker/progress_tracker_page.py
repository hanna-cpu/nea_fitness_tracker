import reflex as rx

from .progress_tracker_state import ProgressTrackerState


def _goal_card(
    title: str,
    has_goal: rx.Var,
    current: rx.Var,
    target: rx.Var,
    pct: rx.Var,
    unit: str,
) -> rx.Component:
    return rx.vstack(
        rx.heading(title, size="4"),
        rx.cond(
            has_goal,
            rx.vstack(
                rx.text(f"{current} / {target} {unit}", size="3", color="gray"),
                rx.progress(value=pct, color_scheme="blue", width="100%"),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text("No goal set yet.", size="3", color="gray"),
                rx.link("Set a goal", href="/fitness-goals", color_scheme="blue"),
                spacing="1",
            ),
        ),
        spacing="3",
        width="100%",
        padding="1.5em",
        border="1px solid var(--gray-6)",
        border_radius="var(--radius-4)",
        align="start",
    )


def progress_tracker() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("Progress Tracker", size="7", color_scheme="blue"),
                rx.spacer(),
                rx.link("Back to Home", href="/home", color_scheme="blue"),
                width="100%",
                align="center",
            ),
            rx.grid(
                _goal_card(
                    "Daily Steps",
                    ProgressTrackerState.has_steps_goal,
                    ProgressTrackerState.steps_current,
                    ProgressTrackerState.steps_target,
                    ProgressTrackerState.steps_pct,
                    "steps",
                ),
                _goal_card(
                    "Workout Duration",
                    ProgressTrackerState.has_workout_goal,
                    ProgressTrackerState.workout_current,
                    ProgressTrackerState.workout_target,
                    ProgressTrackerState.workout_pct,
                    "min",
                ),
                _goal_card(
                    "Weight Goal",
                    ProgressTrackerState.has_weight_goal,
                    ProgressTrackerState.weight_current,
                    ProgressTrackerState.weight_target,
                    ProgressTrackerState.weight_pct,
                    "kg",
                ),
                _goal_card(
                    "Calories Burn",
                    ProgressTrackerState.has_calories_goal,
                    ProgressTrackerState.calories_current,
                    ProgressTrackerState.calories_target,
                    ProgressTrackerState.calories_pct,
                    "kcal",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="5",
            width="50em",
            max_width="95vw",
            padding="2em",
        ),
    )
