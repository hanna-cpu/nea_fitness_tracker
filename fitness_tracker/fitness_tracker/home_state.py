"""Backend logic for the Home page (home_page.py) - today's progress
against each goal, plus the last week or two of data for the trend charts.
"""

from datetime import date, datetime

import reflex as rx

from . import db
from .app_state import State


def _short_date(iso_date: str) -> str:
    """Turn "2026-09-13" into "09/13" - shorter labels for the chart x-axis."""
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%m/%d")


class HomeState(State):
    # "Today so far" vs each goal's target - used in the summary line above
    # each chart, e.g. "6,000 / 10,000 steps today".
    steps_target: float = 0
    steps_current: float = 0

    workout_target: float = 0
    workout_current: float = 0

    calories_target: float = 0
    calories_current: float = 0

    weight_target: float = 0
    weight_start: float = 0  # weight when the goal was first set, for the weight-loss chart
    weight_current: float = 0

    # Data for the four trend charts, e.g. steps_series =
    # [{"date": "09/07", "steps": 4200}, {"date": "09/08", "steps": 6100}, ...]
    weight_series: list[dict] = []
    steps_series: list[dict] = []
    workout_series: list[dict] = []
    calories_series: list[dict] = []

    def load_home(self):
        """Runs every time the Home page is opened - loads everything the
        page needs to display: goal progress, chart data, and notifications.
        """
        if not self.is_logged_in:
            return rx.redirect("/login")

        goals = db.get_goals(self.user_id)
        today = date.today().isoformat()
        summary = db.get_progress_summary(self.user_id, today)
        current_weight = db.get_latest_weight(self.user_id) or 0

        # Only fill in a goal's numbers if the user has actually set one -
        # otherwise the chart card shows "No goal set yet." instead (see
        # home_page.py's has_*_goal checks... actually handled via target=0).
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

        # Build each chart's data by pulling raw rows from the database and
        # reshaping them into the {"date": ..., <value>: ...} dicts the
        # recharts components expect.
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

        # Inherited from the shared State - checks for a "you haven't logged
        # anything today" reminder and refreshes the nav bar's bell icon.
        self.refresh_notifications()
