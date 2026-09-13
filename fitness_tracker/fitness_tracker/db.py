"""Database access layer for the Fitness Tracker app.

This module is the only place in the app that talks to SQLite directly.
Every *_state.py file calls into these functions instead of writing raw SQL
itself - that keeps all the database logic in one place and makes it easier
to test and change later (e.g. swapping SQLite for another database).

It isn't a "page" or a "state" - it's a plain shared utility module that
both frontend pages' state classes import and call into.
"""

import hashlib
import os
import sqlite3
from pathlib import Path

# Path to the actual .db file, worked out relative to this file so it
# doesn't matter what folder the app is run from.
# parents[0] = fitness_tracker/fitness_tracker, parents[1] = fitness_tracker, parents[2] = NEA
DB_PATH = Path(__file__).resolve().parents[2] / "database" / "fitness_tracker.db"


class DuplicateUserError(Exception):
    """Raised when a username or email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when a login attempt fails (wrong username or password)."""


def get_connection() -> sqlite3.Connection:
    """Open a new connection to the database.

    A fresh connection is opened and closed for every function below rather
    than keeping one connection open for the whole app - simpler to reason
    about, and fine for a small single-user-at-a-time app like this.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # SQLite ignores foreign keys unless told to enforce them
    conn.row_factory = sqlite3.Row  # lets us read columns by name, e.g. row["username"]
    return conn


def _hash_password(password: str, salt: bytes | None = None) -> str:
    """Turn a plain-text password into a salted hash that's safe to store.

    Passwords must never be stored in plain text. Here we:
    1. Generate a random 16-byte "salt" (or reuse one, when checking a login).
    2. Run the password through PBKDF2-HMAC-SHA256, 100,000 rounds - this is
       deliberately slow, which makes brute-forcing stolen hashes much harder.
    3. Store the salt and the resulting hash together as "saltHex$hashHex",
       so the salt used for a given user is always available later to
       re-check a login attempt.
    """
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    """Check a login attempt's password against the stored "salt$hash" value."""
    salt_hex, _, _ = stored.partition("$")
    # Re-hash the attempted password with the SAME salt that was used originally,
    # then compare the two hashes. Hashing is one-way, so this is the only way
    # to check a password without ever storing/decrypting the real one.
    return _hash_password(password, bytes.fromhex(salt_hex)) == stored


def create_user(
    username: str,
    password: str,
    email: str,
    name: str,
    date_of_birth: str | None = None,
    gender: str | None = None,
    height_cm: float | None = None,
) -> int:
    """Insert a new row into the User table (used by the Register page).

    Returns the new user's auto-generated user_id so the caller can log the
    user straight in after registering.
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            INSERT INTO User (username, password_hash, email, name, date_of_birth, gender, height_cm)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (username, _hash_password(password), email, name, date_of_birth, gender, height_cm),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        # The User table has UNIQUE constraints on username and email, so this
        # error means one of those is already taken.
        raise DuplicateUserError("That username or email is already registered.") from e
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> sqlite3.Row:
    """Check a username/password pair and return the matching User row.

    Raises InvalidCredentialsError if the username doesn't exist or the
    password is wrong - deliberately the same error either way, so a failed
    login attempt can't be used to guess which usernames exist.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM User WHERE username = ?", (username,)
        ).fetchone()
        if row is None or not _verify_password(password, row["password_hash"]):
            raise InvalidCredentialsError("Incorrect username or password.")
        return row
    finally:
        conn.close()


def get_user(user_id: int) -> sqlite3.Row | None:
    """Fetch one user's full row, e.g. to pre-fill the Account Settings form."""
    conn = get_connection()
    try:
        return conn.execute("SELECT * FROM User WHERE user_id = ?", (user_id,)).fetchone()
    finally:
        conn.close()


def update_user(
    user_id: int,
    name: str,
    email: str,
    gender: str | None,
    height_cm: float | None,
    date_of_birth: str | None,
) -> None:
    """Save changes made on the Account Settings page."""
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE User
            SET name = ?, email = ?, gender = ?, height_cm = ?, date_of_birth = ?
            WHERE user_id = ?
            """,
            (name, email, gender, height_cm, date_of_birth, user_id),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        # Email has a UNIQUE constraint too, so this fires if it now clashes
        # with someone else's email.
        raise DuplicateUserError("That email is already registered.") from e
    finally:
        conn.close()


# --- Adding new fitness data (Add Fitness Data page) -----------------------
# One simple "insert a new row" function per table. Each entry is its own
# row rather than overwriting anything, so a full history builds up over time.

def add_workout_record(user_id: int, workout_type: str, duration_minutes: int, date: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO WorkoutRecord (user_id, workout_type, duration_minutes, date) VALUES (?, ?, ?, ?)",
            (user_id, workout_type, duration_minutes, date),
        )
        conn.commit()
    finally:
        conn.close()


def add_weight_record(user_id: int, weight_kg: float, date: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO WeightRecord (user_id, weight_kg, date) VALUES (?, ?, ?)",
            (user_id, weight_kg, date),
        )
        conn.commit()
    finally:
        conn.close()


def add_calorie_record(
    user_id: int, calories_consumed: int | None, calories_burned: int | None, date: str
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO CalorieRecord (user_id, calories_consumed, calories_burned, date) VALUES (?, ?, ?, ?)",
            (user_id, calories_consumed, calories_burned, date),
        )
        conn.commit()
    finally:
        conn.close()


def add_step_record(user_id: int, step_count: int, date: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO StepRecord (user_id, step_count, date) VALUES (?, ?, ?)",
            (user_id, step_count, date),
        )
        conn.commit()
    finally:
        conn.close()


# --- Reading history (History page) ----------------------------------------
# One "get everything for this user, newest first" function per table.

def get_workout_history(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT date, workout_type, duration_minutes FROM WorkoutRecord "
            "WHERE user_id = ? ORDER BY date DESC, workout_id DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def get_weight_history(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT date, weight_kg FROM WeightRecord "
            "WHERE user_id = ? ORDER BY date DESC, weight_id DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def get_calorie_history(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT date, calories_consumed, calories_burned FROM CalorieRecord "
            "WHERE user_id = ? ORDER BY date DESC, calorie_id DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def get_step_history(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT date, step_count FROM StepRecord "
            "WHERE user_id = ? ORDER BY date DESC, step_id DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


# --- Goals (Fitness Goals page) ---------------------------------------------

def upsert_goal(
    user_id: int,
    goal_type: str,
    target_value: float,
    start_value: float | None,
    start_date: str,
    target_date: str | None,
) -> None:
    """Create or update a user's goal for one goal_type (steps/workout_duration/weight/calories).

    Unlike the "add a record" functions above, goals aren't a history - a
    user only has ONE current goal per type. The Goal table has a UNIQUE
    constraint on (user_id, goal_type), so "INSERT ... ON CONFLICT DO UPDATE"
    inserts a new goal the first time, and just updates the existing one
    every time after that, instead of creating duplicate rows.
    """
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO Goal (user_id, goal_type, target_value, start_value, start_date, target_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, goal_type) DO UPDATE SET
                target_value = excluded.target_value,
                start_value = excluded.start_value,
                start_date = excluded.start_date,
                target_date = excluded.target_date
            """,
            (user_id, goal_type, target_value, start_value, start_date, target_date),
        )
        conn.commit()
    finally:
        conn.close()


def get_goals(user_id: int) -> dict[str, sqlite3.Row]:
    """All of a user's goals, keyed by goal_type for easy lookup, e.g. goals["steps"]."""
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM Goal WHERE user_id = ?", (user_id,)).fetchall()
        return {row["goal_type"]: row for row in rows}
    finally:
        conn.close()


def get_latest_weight(user_id: int) -> float | None:
    """The user's most recently logged weight, or None if they've never logged one."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT weight_kg FROM WeightRecord WHERE user_id = ? ORDER BY date DESC, weight_id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return row["weight_kg"] if row else None
    finally:
        conn.close()


def get_progress_summary(user_id: int, today: str) -> dict:
    """Today's totals (steps walked, minutes worked out, calories burned) -
    used on the Home page to compare "today so far" against each goal.
    """
    conn = get_connection()
    try:
        steps_today = conn.execute(
            "SELECT COALESCE(SUM(step_count), 0) FROM StepRecord WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()[0]
        workout_minutes_today = conn.execute(
            "SELECT COALESCE(SUM(duration_minutes), 0) FROM WorkoutRecord WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()[0]
        calories_burned_today = conn.execute(
            "SELECT COALESCE(SUM(calories_burned), 0) FROM CalorieRecord WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()[0]
        return {
            "steps_today": steps_today,
            "workout_minutes_today": workout_minutes_today,
            "calories_burned_today": calories_burned_today,
        }
    finally:
        conn.close()


def _last_n_dates(days: int) -> list[str]:
    """The last `days` calendar dates as ISO strings, oldest first, ending today.

    e.g. _last_n_dates(3) on 2026-09-13 -> ["2026-09-11", "2026-09-12", "2026-09-13"]
    Used to build the trend charts on the Home page so every day in the
    range appears on the x-axis, even days with no data logged (those get
    filled in with 0 further down).
    """
    from datetime import date, timedelta

    today = date.today()
    return [(today - timedelta(days=i)).isoformat() for i in range(days - 1, -1, -1)]


def get_weight_series(user_id: int, limit: int = 14) -> list[sqlite3.Row]:
    """Chronological (oldest -> newest) weight entries, for the weight trend chart."""
    conn = get_connection()
    try:
        # Fetch the most recent `limit` entries (newest first), then reverse
        # them so the chart reads left-to-right in time order.
        rows = conn.execute(
            "SELECT date, weight_kg FROM WeightRecord WHERE user_id = ? "
            "ORDER BY date DESC, weight_id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return list(reversed(rows))
    finally:
        conn.close()


def get_daily_steps_series(user_id: int, days: int = 7) -> list[dict]:
    """Total steps per day for the last `days` days, for the steps bar chart.

    Days with no StepRecord logged still appear in the result with steps=0,
    so the chart doesn't just skip gaps in the data.
    """
    conn = get_connection()
    try:
        dates = _last_n_dates(days)
        rows = conn.execute(
            "SELECT date, SUM(step_count) AS total FROM StepRecord "
            "WHERE user_id = ? AND date >= ? GROUP BY date",
            (user_id, dates[0]),
        ).fetchall()
        totals = {row["date"]: row["total"] for row in rows}
        return [{"date": d, "steps": totals.get(d, 0)} for d in dates]
    finally:
        conn.close()


def get_daily_workout_minutes_series(user_id: int, days: int = 7) -> list[dict]:
    """Total workout minutes per day for the last `days` days (same zero-filling idea)."""
    conn = get_connection()
    try:
        dates = _last_n_dates(days)
        rows = conn.execute(
            "SELECT date, SUM(duration_minutes) AS total FROM WorkoutRecord "
            "WHERE user_id = ? AND date >= ? GROUP BY date",
            (user_id, dates[0]),
        ).fetchall()
        totals = {row["date"]: row["total"] for row in rows}
        return [{"date": d, "minutes": totals.get(d, 0)} for d in dates]
    finally:
        conn.close()


def get_daily_calories_series(user_id: int, days: int = 7) -> list[dict]:
    """Consumed vs burned calories per day for the last `days` days."""
    conn = get_connection()
    try:
        dates = _last_n_dates(days)
        rows = conn.execute(
            "SELECT date, SUM(calories_consumed) AS consumed, SUM(calories_burned) AS burned "
            "FROM CalorieRecord WHERE user_id = ? AND date >= ? GROUP BY date",
            (user_id, dates[0]),
        ).fetchall()
        totals = {row["date"]: (row["consumed"] or 0, row["burned"] or 0) for row in rows}
        return [
            {
                "date": d,
                "consumed": totals.get(d, (0, 0))[0],
                "burned": totals.get(d, (0, 0))[1],
            }
            for d in dates
        ]
    finally:
        conn.close()


# --- Notifications -----------------------------------------------------------

def has_logged_activity_today(user_id: int, today: str) -> bool:
    """True if the user has logged a workout, weight, calorie or step entry today.

    Used to decide whether to nag them with an activity reminder.
    """
    conn = get_connection()
    try:
        # EXISTS is faster than COUNT here since it can stop as soon as it finds
        # one matching row in any of the four tables, instead of counting them all.
        row = conn.execute(
            """
            SELECT
                EXISTS(SELECT 1 FROM WorkoutRecord WHERE user_id = ? AND date = ?)
                OR EXISTS(SELECT 1 FROM WeightRecord WHERE user_id = ? AND date = ?)
                OR EXISTS(SELECT 1 FROM CalorieRecord WHERE user_id = ? AND date = ?)
                OR EXISTS(SELECT 1 FROM StepRecord WHERE user_id = ? AND date = ?)
            """,
            (user_id, today, user_id, today, user_id, today, user_id, today),
        ).fetchone()
        return bool(row[0])
    finally:
        conn.close()


def create_notification(user_id: int, type: str, message: str) -> None:
    """Insert a new row into the Notification table."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO Notification (user_id, type, message) VALUES (?, ?, ?)",
            (user_id, type, message),
        )
        conn.commit()
    finally:
        conn.close()


def ensure_daily_activity_reminder(user_id: int, today: str) -> None:
    """Create today's "no activity logged" reminder - but only once.

    This runs every time a logged-in page loads, so without the duplicate
    check below it would create a brand new notification on every single
    page visit. Instead: if the user has already logged something today,
    or a reminder for today already exists, do nothing.
    """
    if has_logged_activity_today(user_id, today):
        return
    conn = get_connection()
    try:
        already_sent = conn.execute(
            """
            SELECT 1 FROM Notification
            WHERE user_id = ? AND type = 'activity_reminder' AND date(date_created) = ?
            """,
            (user_id, today),
        ).fetchone()
        if already_sent:
            return
    finally:
        conn.close()
    create_notification(
        user_id,
        "activity_reminder",
        "You haven't logged any activity today. Add your workout, weight, calories or steps to stay on track!",
    )


def get_unread_notifications(user_id: int) -> list[sqlite3.Row]:
    """Notifications the user hasn't dismissed yet, newest first."""
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM Notification WHERE user_id = ? AND is_read = 0 "
            "ORDER BY date_created DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def mark_notification_read(notification_id: int) -> None:
    """Mark one notification as read/dismissed, e.g. after the user clicks its X button."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE Notification SET is_read = 1 WHERE notification_id = ?",
            (notification_id,),
        )
        conn.commit()
    finally:
        conn.close()
