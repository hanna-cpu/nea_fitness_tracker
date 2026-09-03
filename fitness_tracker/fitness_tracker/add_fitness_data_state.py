from datetime import date

import reflex as rx

from . import db
from .app_state import State

WORKOUT_TYPES = ["Running", "Cycling", "Swimming", "Weight Training", "Yoga", "Other"]


class AddFitnessDataState(State):
    workout_type: str = ""
    workout_duration: str = ""
    workout_date: str = ""
    workout_message: str = ""

    weight_value: str = ""
    weight_date: str = ""
    weight_message: str = ""

    calories_consumed: str = ""
    calories_burned: str = ""
    calories_date: str = ""
    calories_message: str = ""

    steps_value: str = ""
    steps_date: str = ""
    steps_message: str = ""

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
        if not self.is_logged_in:
            return rx.redirect("/login")
        today = date.today().isoformat()
        self.workout_date = today
        self.weight_date = today
        self.calories_date = today
        self.steps_date = today

    def save_workout(self):
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
        self.workout_message = "Saved."

    def save_weight(self):
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
        self.weight_message = "Saved."

    def save_calories(self):
        self.calories_message = ""
        if not self.calories_date:
            self.calories_message = "Pick a date."
            return
        try:
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
        self.calories_message = "Saved."

    def save_steps(self):
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
        self.steps_message = "Saved."
