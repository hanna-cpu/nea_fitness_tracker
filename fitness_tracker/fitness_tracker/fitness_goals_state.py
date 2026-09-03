from datetime import date

import reflex as rx

from . import db
from .app_state import State


class FitnessGoalsState(State):
    workout_duration_goal: str = ""
    weight_goal: str = ""
    calories_goal: str = ""
    steps_goal: str = ""
    message: str = ""

    def set_workout_duration_goal(self, value: str):
        self.workout_duration_goal = value

    def set_weight_goal(self, value: str):
        self.weight_goal = value

    def set_calories_goal(self, value: str):
        self.calories_goal = value

    def set_steps_goal(self, value: str):
        self.steps_goal = value

    def load_goals(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
        goals = db.get_goals(self.user_id)
        if "workout_duration" in goals:
            self.workout_duration_goal = str(goals["workout_duration"]["target_value"])
        if "weight" in goals:
            self.weight_goal = str(goals["weight"]["target_value"])
        if "calories" in goals:
            self.calories_goal = str(goals["calories"]["target_value"])
        if "steps" in goals:
            self.steps_goal = str(goals["steps"]["target_value"])

    def save_workout_duration_goal(self):
        self.message = ""
        try:
            target = float(self.workout_duration_goal)
        except ValueError:
            self.message = "Workout duration goal must be a number."
            return
        db.upsert_goal(self.user_id, "workout_duration", target, None, date.today().isoformat(), None)
        self.message = "Goals saved."

    def save_weight_goal(self):
        self.message = ""
        try:
            target = float(self.weight_goal)
        except ValueError:
            self.message = "Weight goal must be a number."
            return
        current_weight = db.get_latest_weight(self.user_id)
        db.upsert_goal(
            self.user_id, "weight", target, current_weight, date.today().isoformat(), None
        )
        self.message = "Goals saved."

    def save_calories_goal(self):
        self.message = ""
        try:
            target = float(self.calories_goal)
        except ValueError:
            self.message = "Calories goal must be a number."
            return
        db.upsert_goal(self.user_id, "calories", target, None, date.today().isoformat(), None)
        self.message = "Goals saved."

    def save_steps_goal(self):
        self.message = ""
        try:
            target = float(self.steps_goal)
        except ValueError:
            self.message = "Steps goal must be a number."
            return
        db.upsert_goal(self.user_id, "steps", target, None, date.today().isoformat(), None)
        self.message = "Goals saved."
