from datetime import date, datetime

import reflex as rx

from . import db
from .app_state import State


def _short_date(iso_date: str) -> str:
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%m/%d")


class HomeState(State):
    steps_target: float = 0
    steps_current: float = 0

    workout_target: float = 0
    workout_current: float = 0

    calories_target: float = 0
    calories_current: float = 0

    weight_target: float = 0
    weight_start: float = 0
    weight_current: float = 0

    weight_series: list[dict] = []
    steps_series: list[dict] = []
    workout_series: list[dict] = []
    calories_series: list[dict] = []

    def load_home(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

        goals = db.get_goals(self.user_id)
        today = date.today().isoformat()
        summary = db.get_progress_summary(self.user_id, today)
        current_weight = db.get_latest_weight(self.user_id) or 0

        if "steps" in goals:
            self.steps_target = goals["steps"]["target_value"]
            self.steps_current = summary["steps_today"]

        if "workout_duration" in goals:
            self.workout_target = goals["workout_duration"]["target_value"]
            self.workout_current = summary["workout_minutes_today"]

        if "calories" in goals:
            self.calories_target = goals["calories"]["target_value"]
            self.calories_current = summary["calories_burned_today"]

        if "weight" in goals:
            self.weight_target = goals["weight"]["target_value"]
            self.weight_start = goals["weight"]["start_value"] or current_weight
            self.weight_current = current_weight

        self.weight_series = [
            {"date": _short_date(row["date"]), "weight": row["weight_kg"]}
            for row in db.get_weight_series(self.user_id)
        ]
        self.steps_series = [
            {"date": _short_date(row["date"]), "steps": row["steps"]}
            for row in db.get_daily_steps_series(self.user_id)
        ]
        self.workout_series = [
            {"date": _short_date(row["date"]), "minutes": row["minutes"]}
            for row in db.get_daily_workout_minutes_series(self.user_id)
        ]
        self.calories_series = [
            {
                "date": _short_date(row["date"]),
                "consumed": row["consumed"],
                "burned": row["burned"],
            }
            for row in db.get_daily_calories_series(self.user_id)
        ]

        self.refresh_notifications()
