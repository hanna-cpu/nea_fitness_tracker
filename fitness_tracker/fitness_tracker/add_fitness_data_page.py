import reflex as rx

from .add_fitness_data_state import WORKOUT_TYPES, AddFitnessDataState
from .nav_bar import nav_bar


def _field(label: str, input_component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        input_component,
        spacing="1",
        width="100%",
        align="start",
    )


def _data_dialog(
    icon: str,
    trigger_label: str,
    dialog_title: str,
    is_open: rx.Var,
    on_open_change,
    on_save,
    message: rx.Var,
    *fields: rx.Component,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(icon, size=18),
                trigger_label,
                size="4",
                color_scheme="violet",
                width="12em",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.icon(icon, size=20, color="var(--violet-9)"),
                rx.dialog.title(dialog_title, margin_bottom="0"),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                *fields,
                rx.cond(
                    message != "",
                    rx.callout(message, color_scheme="red", width="100%"),
                ),
                rx.hstack(
                    rx.dialog.close(rx.button("Cancel", variant="soft", color_scheme="gray")),
                    rx.button("Save", on_click=on_save, color_scheme="violet"),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            max_width="28em",
        ),
        open=is_open,
        on_open_change=on_open_change,
    )


def add_fitness_data() -> rx.Component:
    return rx.vstack(
        nav_bar(),
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.icon("clipboard_plus", size=28, color="var(--violet-9)"),
                    rx.heading("Add Fitness Data", size="7", color_scheme="violet"),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    "Pick a category to log today's data.",
                    size="3",
                    color="gray",
                ),
                rx.grid(
                    _data_dialog(
                        "dumbbell",
                        "Workout",
                        "Add Workout",
                        AddFitnessDataState.workout_dialog_open,
                        AddFitnessDataState.set_workout_dialog_open,
                        AddFitnessDataState.save_workout,
                        AddFitnessDataState.workout_message,
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
                    ),
                    _data_dialog(
                        "scale",
                        "Weight",
                        "Add Weight",
                        AddFitnessDataState.weight_dialog_open,
                        AddFitnessDataState.set_weight_dialog_open,
                        AddFitnessDataState.save_weight,
                        AddFitnessDataState.weight_message,
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
                    ),
                    _data_dialog(
                        "flame",
                        "Calories",
                        "Add Calories",
                        AddFitnessDataState.calories_dialog_open,
                        AddFitnessDataState.set_calories_dialog_open,
                        AddFitnessDataState.save_calories,
                        AddFitnessDataState.calories_message,
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
                    ),
                    _data_dialog(
                        "footprints",
                        "Steps",
                        "Add Steps",
                        AddFitnessDataState.steps_dialog_open,
                        AddFitnessDataState.set_steps_dialog_open,
                        AddFitnessDataState.save_steps,
                        AddFitnessDataState.steps_message,
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
                    ),
                    columns="2",
                    spacing="4",
                ),
                spacing="5",
                padding="2em",
            ),
        ),
        width="100%",
        spacing="0",
        align="center",
        min_height="100vh",
        background="linear-gradient(135deg, var(--blue-3), var(--purple-3))",
    )
