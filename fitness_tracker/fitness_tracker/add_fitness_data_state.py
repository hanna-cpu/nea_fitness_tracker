"""Backend logic for the Add Fitness Data page (add_fitness_data_page.py) -
four separate pop-up forms (Workout/Weight/Calories/Steps), each saving to
its own table.
"""

from datetime import date

import reflex as rx

from . import db
from .app_state import State

# Fixed list of choices for the "Workout Type" dropdown.
WORKOUT_TYPES = ["Running", "Cycling", "Swimming", "Weight Training", "Yoga", "Other"]


class AddFitnessDataState(State):
    # Whether each of the four pop-up dialogs is currently open. Reflex
    # controls the dialog with these, rather than letting the dialog manage
    # its own open/closed state - that's what lets save_workout() etc. close
    # the dialog automatically once saving succeeds.
    workout_dialog_open: bool = False
    weight_dialog_open: bool = False
    calories_dialog_open: bool = False
    steps_dialog_open: bool = False

    # Workout dialog fields.
    workout_type: str = ""
    workout_duration: str = ""
    workout_date: str = ""
    workout_message: str = ""  # error message shown inside the dialog

    # Weight dialog fields.
    weight_value: str = ""
    weight_date: str = ""
    weight_message: str = ""

    # Calories dialog fields.
    calories_consumed: str = ""
    calories_burned: str = ""
    calories_date: str = ""
    calories_message: str = ""

    # Steps dialog fields.
    steps_value: str = ""
    steps_date: str = ""
    steps_message: str = ""

    def set_workout_dialog_open(self, value: bool):
        self.workout_dialog_open = value
        self.workout_message = ""  # clear any old error when opening/closing

    def set_weight_dialog_open(self, value: bool):
        self.weight_dialog_open = value
        self.weight_message = ""

    def set_calories_dialog_open(self, value: bool):
        self.calories_dialog_open = value
        self.calories_message = ""

    def set_steps_dialog_open(self, value: bool):
        self.steps_dialog_open = value
        self.steps_message = ""

    def set_workout_type(self, value: str):
        self.workout_type = value

    def set_workout_duration(self, value: str):
        self.workout_duration = value

    def set_workout_date(self, value: str):
        self.workout_date = value

    def set_weight_value(self, value: str):
        self.weight_value = value

    def set_weight_date(self, value: str):
        self.weight_date = value

    def set_calories_consumed(self, value: str):
        self.calories_consumed = value

    def set_calories_burned(self, value: str):
        self.calories_burned = value

    def set_calories_date(self, value: str):
        self.calories_date = value

    def set_steps_value(self, value: str):
        self.steps_value = value

    def set_steps_date(self, value: str):
        self.steps_date = value

    def load_defaults(self):
        """Runs when the page loads - pre-fills all four date fields with
        today's date, so the user doesn't have to type it in every time.
        """
        if not self.is_logged_in:
            return rx.redirect("/login")
        today = date.today().isoformat()
        self.workout_date = today
        self.weight_date = today
        self.calories_date = today
        self.steps_date = today

    def save_workout(self):
        """Runs when Save is clicked in the Workout dialog."""
        self.workout_message = ""
        if not (self.workout_type and self.workout_duration and self.workout_date):
            self.workout_message = "Fill in workout type, duration and date."
            return
        try:
            duration = int(self.workout_duration)
        except ValueError:
            self.workout_message = "Duration must be a whole number."
            return
        db.add_workout_record(self.user_id, self.workout_type, duration, self.workout_date)
        self.workout_duration = ""
        self.workout_message = ""
        self.workout_dialog_open = False  # close the dialog on success

    def save_weight(self):
        """Runs when Save is clicked in the Weight dialog."""
        self.weight_message = ""
        if not (self.weight_value and self.weight_date):
            self.weight_message = "Fill in weight and date."
            return
        try:
            weight = float(self.weight_value)
        except ValueError:
            self.weight_message = "Weight must be a number."
            return
        db.add_weight_record(self.user_id, weight, self.weight_date)
        self.weight_value = ""
        self.weight_message = ""
        self.weight_dialog_open = False

    def save_calories(self):
        """Runs when Save is clicked in the Calories dialog."""
        self.calories_message = ""
        if not self.calories_date:
            self.calories_message = "Pick a date."
            return
        try:
            # Both fields are optional - only convert the ones the user
            # actually filled in.
            consumed = int(self.calories_consumed) if self.calories_consumed else None
            burned = int(self.calories_burned) if self.calories_burned else None
        except ValueError:
            self.calories_message = "Calories must be whole numbers."
            return
        if consumed is None and burned is None:
            self.calories_message = "Enter consumed and/or burned calories."
            return
        db.add_calorie_record(self.user_id, consumed, burned, self.calories_date)
        self.calories_consumed = ""
        self.calories_burned = ""
        self.calories_message = ""
        self.calories_dialog_open = False

    def save_steps(self):
        """Runs when Save is clicked in the Steps dialog."""
        self.steps_message = ""
        if not (self.steps_value and self.steps_date):
            self.steps_message = "Fill in step count and date."
            return
        try:
            steps = int(self.steps_value)
        except ValueError:
            self.steps_message = "Steps must be a whole number."
            return
        db.add_step_record(self.user_id, steps, self.steps_date)
        self.steps_value = ""
        self.steps_message = ""
        self.steps_dialog_open = False
