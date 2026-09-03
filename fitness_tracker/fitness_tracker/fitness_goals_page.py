import reflex as rx

from .fitness_goals_state import FitnessGoalsState


def _goal_row(label: str, value: rx.Var, on_change, on_save, unit: str) -> rx.Component:
    return rx.hstack(
        rx.text(label, size="3", width="12em"),
        rx.input(
            type="number",
            value=value,
            on_change=on_change,
            placeholder=unit,
            width="10em",
        ),
        rx.button("Save", on_click=on_save, color_scheme="blue"),
        spacing="3",
        align="center",
        width="100%",
    )


def fitness_goals() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("Fitness Goals", size="7", color_scheme="blue"),
                rx.spacer(),
                rx.link("Back to Home", href="/home", color_scheme="blue"),
                width="100%",
                align="center",
            ),
            rx.cond(
                FitnessGoalsState.message != "",
                rx.callout(FitnessGoalsState.message, color_scheme="green", width="100%"),
            ),
            _goal_row(
                "Daily Steps",
                FitnessGoalsState.steps_goal,
                FitnessGoalsState.set_steps_goal,
                FitnessGoalsState.save_steps_goal,
                "steps",
            ),
            _goal_row(
                "Workout Duration",
                FitnessGoalsState.workout_duration_goal,
                FitnessGoalsState.set_workout_duration_goal,
                FitnessGoalsState.save_workout_duration_goal,
                "minutes",
            ),
            _goal_row(
                "Weight Goal",
                FitnessGoalsState.weight_goal,
                FitnessGoalsState.set_weight_goal,
                FitnessGoalsState.save_weight_goal,
                "kg",
            ),
            _goal_row(
                "Daily Calories Burn",
                FitnessGoalsState.calories_goal,
                FitnessGoalsState.set_calories_goal,
                FitnessGoalsState.save_calories_goal,
                "kcal",
            ),
            spacing="5",
            width="34em",
            padding="2em",
            border="1px solid var(--gray-6)",
            border_radius="var(--radius-4)",
        ),
    )
