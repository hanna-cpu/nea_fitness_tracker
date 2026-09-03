import reflex as rx

from . import db
from .app_state import State


class HistoryState(State):
    workout_history: list[dict[str, str]] = []
    weight_history: list[dict[str, str]] = []
    calorie_history: list[dict[str, str]] = []
    step_history: list[dict[str, str]] = []

    def load_history(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

        self.workout_history = [
            {
                "date": row["date"],
                "workout_type": row["workout_type"],
                "duration": f"{row['duration_minutes']} min",
            }
            for row in db.get_workout_history(self.user_id)
        ]

        weight_rows = db.get_weight_history(self.user_id)
        weight_list = []
        for i, row in enumerate(weight_rows):
            if i + 1 < len(weight_rows):
                change = row["weight_kg"] - weight_rows[i + 1]["weight_kg"]
                change_str = f"{change:+.1f} kg"
            else:
                change_str = "-"
            weight_list.append({
                "date": row["date"],
                "weight": f"{row['weight_kg']:.1f} kg",
                "change": change_str,
            })
        self.weight_history = weight_list

        self.calorie_history = [
            {
                "date": row["date"],
                "consumed": str(row["calories_consumed"]) if row["calories_consumed"] is not None else "-",
                "burned": str(row["calories_burned"]) if row["calories_burned"] is not None else "-",
            }
            for row in db.get_calorie_history(self.user_id)
        ]

        goals = db.get_goals(self.user_id)
        steps_goal = str(int(goals["steps"]["target_value"])) if "steps" in goals else "-"
        self.step_history = [
            {
                "date": row["date"],
                "steps": str(row["step_count"]),
                "daily_goal": steps_goal,
            }
            for row in db.get_step_history(self.user_id)
        ]
