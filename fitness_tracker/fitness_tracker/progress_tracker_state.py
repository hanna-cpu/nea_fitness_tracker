from datetime import date

import reflex as rx

from . import db
from .app_state import State


def _pct(current: float, target: float) -> int:
    if not target:
        return 0
    return max(0, min(100, round(current / target * 100)))


class ProgressTrackerState(State):
    has_steps_goal: bool = False
    steps_target: float = 0
    steps_current: float = 0
    steps_pct: int = 0

    has_workout_goal: bool = False
    workout_target: float = 0
    workout_current: float = 0
    workout_pct: int = 0

    has_calories_goal: bool = False
    calories_target: float = 0
    calories_current: float = 0
    calories_pct: int = 0

    has_weight_goal: bool = False
    weight_target: float = 0
    weight_start: float = 0
    weight_current: float = 0
    weight_pct: int = 0

    def load_progress(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

        goals = db.get_goals(self.user_id)
        today = date.today().isoformat()
        summary = db.get_progress_summary(self.user_id, today)
        current_weight = db.get_latest_weight(self.user_id) or 0

        if "steps" in goals:
            self.has_steps_goal = True
            self.steps_target = goals["steps"]["target_value"]
            self.steps_current = summary["steps_today"]
            self.steps_pct = _pct(self.steps_current, self.steps_target)

        if "workout_duration" in goals:
            self.has_workout_goal = True
            self.workout_target = goals["workout_duration"]["target_value"]
            self.workout_current = summary["workout_minutes_today"]
            self.workout_pct = _pct(self.workout_current, self.workout_target)

        if "calories" in goals:
            self.has_calories_goal = True
            self.calories_target = goals["calories"]["target_value"]
            self.calories_current = summary["calories_burned_today"]
            self.calories_pct = _pct(self.calories_current, self.calories_target)

        if "weight" in goals:
            self.has_weight_goal = True
            self.weight_target = goals["weight"]["target_value"]
            self.weight_start = goals["weight"]["start_value"] or current_weight
            self.weight_current = current_weight
            total_change_needed = self.weight_start - self.weight_target
            progress_so_far = self.weight_start - self.weight_current
            self.weight_pct = _pct(progress_so_far, total_change_needed)
