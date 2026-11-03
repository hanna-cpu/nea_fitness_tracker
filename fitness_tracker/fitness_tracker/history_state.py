"""Backend logic for the History page (history_page.py) - builds the four
tables (Workout/Weight/Calories/Steps) shown there.
"""

import reflex as rx

from . import db
from .app_state import State


class HistoryState(State):
    # Each list holds one dict per table row, already formatted as strings
    # ready to display - e.g. workout_history =
    # [{"date": "2026-09-13", "workout_type": "Running", "duration": "30 min"}, ...]
    workout_history: list[dict[str, str]] = []
    weight_history: list[dict[str, str]] = []
    calorie_history: list[dict[str, str]] = []
    step_history: list[dict[str, str]] = []

    def load_history(self):
        """Runs when the page loads - fetches all four histories and turns
        the raw database rows into display-ready text.
        """
        if self.user_id <= 0:
            return rx.redirect("/login")

        self.workout_history = [
            {
                "date": row["date"],
                "workout_type": row["workout_type"],
                "duration": f"{row['duration_minutes']} min",
            }
            for row in db.get_workout_history(self.user_id)
        ]

        # The weight table also shows how much the weight changed since the
        # entry before it. The rows come back newest-first, so the "previous"
        # entry (the older weigh-in) is the next one along in the list.
        weight_rows = db.get_weight_history(self.user_id)
        weight_list = []
        for position in range(len(weight_rows)):
            this_weight = weight_rows[position]["weight_kg"]

            # Work out the change compared with the older entry, if there is one.
            is_oldest_entry = (position == len(weight_rows) - 1)
            if is_oldest_entry:
                change_str = "-"  # nothing older to compare against
            else:
                older_weight = weight_rows[position + 1]["weight_kg"]
                change = this_weight - older_weight
                sign = "+" if change >= 0 else "-"  # always show the sign, e.g. "+1.2 kg"
                change_str = f"{sign}{abs(change):.1f} kg"

            weight_list.append({
                "date": weight_rows[position]["date"],
                "weight": f"{this_weight:.1f} kg",
                "change": change_str,
            })
        self.weight_history = weight_list

        self.calorie_history = [
            {
                "date": row["date"],
                # calories_consumed/burned can be NULL if only one was logged that day
                "consumed": str(row["calories_consumed"]) if row["calories_consumed"] is not None else "-",
                "burned": str(row["calories_burned"]) if row["calories_burned"] is not None else "-",
            }
            for row in db.get_calorie_history(self.user_id)
        ]

        # The steps table also shows the user's current daily step goal
        # alongside each entry, for quick comparison.
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
