import reflex as rx

from .add_fitness_data_state import WORKOUT_TYPES, AddFitnessDataState


def _panel(*children: rx.Component) -> rx.Component:
    return rx.vstack(
        *children,
        spacing="3",
        width="100%",
        padding="1.5em",
        border="1px solid var(--gray-6)",
        border_radius="var(--radius-4)",
        align="start",
    )


def _field(label: str, input_component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        input_component,
        spacing="1",
        width="100%",
        align="start",
    )


def add_fitness_data() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("Add Fitness Data", size="7", color_scheme="blue"),
                rx.spacer(),
                rx.link("Back to Home", href="/home", color_scheme="blue"),
                width="100%",
                align="center",
            ),
            rx.grid(
                _panel(
                    rx.heading("Workout", size="4"),
                    _field(
                        "Workout Type",
                        rx.select(
                            WORKOUT_TYPES,
                            value=AddFitnessDataState.workout_type,
                            on_change=AddFitnessDataState.set_workout_type,
                            placeholder="Select type",
                            width="100%",
                        ),
                    ),
                    _field(
                        "Duration (minutes)",
                        rx.input(
                            type="number",
                            value=AddFitnessDataState.workout_duration,
                            on_change=AddFitnessDataState.set_workout_duration,
                            width="100%",
                        ),
                    ),
                    _field(
                        "Date",
                        rx.input(
                            type="date",
                            value=AddFitnessDataState.workout_date,
                            on_change=AddFitnessDataState.set_workout_date,
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        AddFitnessDataState.workout_message != "",
                        rx.text(AddFitnessDataState.workout_message, size="2", color="gray"),
                    ),
                    rx.button(
                        "Save",
                        on_click=AddFitnessDataState.save_workout,
                        color_scheme="blue",
                        width="100%",
                    ),
                ),
                _panel(
                    rx.heading("Weight", size="4"),
                    _field(
                        "Weight (kg)",
                        rx.input(
                            type="number",
                            value=AddFitnessDataState.weight_value,
                            on_change=AddFitnessDataState.set_weight_value,
                            width="100%",
                        ),
                    ),
                    _field(
                        "Date",
                        rx.input(
                            type="date",
                            value=AddFitnessDataState.weight_date,
                            on_change=AddFitnessDataState.set_weight_date,
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        AddFitnessDataState.weight_message != "",
                        rx.text(AddFitnessDataState.weight_message, size="2", color="gray"),
                    ),
                    rx.button(
                        "Save",
                        on_click=AddFitnessDataState.save_weight,
                        color_scheme="blue",
                        width="100%",
                    ),
                ),
                _panel(
                    rx.heading("Calories", size="4"),
                    _field(
                        "Calories Consumed (kcal)",
                        rx.input(
                            type="number",
                            value=AddFitnessDataState.calories_consumed,
                            on_change=AddFitnessDataState.set_calories_consumed,
                            width="100%",
                        ),
                    ),
                    _field(
                        "Calories Burned (kcal)",
                        rx.input(
                            type="number",
                            value=AddFitnessDataState.calories_burned,
                            on_change=AddFitnessDataState.set_calories_burned,
                            width="100%",
                        ),
                    ),
                    _field(
                        "Date",
                        rx.input(
                            type="date",
                            value=AddFitnessDataState.calories_date,
                            on_change=AddFitnessDataState.set_calories_date,
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        AddFitnessDataState.calories_message != "",
                        rx.text(AddFitnessDataState.calories_message, size="2", color="gray"),
                    ),
                    rx.button(
                        "Save",
                        on_click=AddFitnessDataState.save_calories,
                        color_scheme="blue",
                        width="100%",
                    ),
                ),
                _panel(
                    rx.heading("Steps", size="4"),
                    _field(
                        "Step Count",
                        rx.input(
                            type="number",
                            value=AddFitnessDataState.steps_value,
                            on_change=AddFitnessDataState.set_steps_value,
                            width="100%",
                        ),
                    ),
                    _field(
                        "Date",
                        rx.input(
                            type="date",
                            value=AddFitnessDataState.steps_date,
                            on_change=AddFitnessDataState.set_steps_date,
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        AddFitnessDataState.steps_message != "",
                        rx.text(AddFitnessDataState.steps_message, size="2", color="gray"),
                    ),
                    rx.button(
                        "Save",
                        on_click=AddFitnessDataState.save_steps,
                        color_scheme="blue",
                        width="100%",
                    ),
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="5",
            width="60em",
            max_width="95vw",
            padding="2em",
        ),
    )
