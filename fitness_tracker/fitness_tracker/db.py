"""Shared SQLite access. Not a page or a state - a plain utility both states call into."""

import hashlib
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "database" / "fitness_tracker.db"


class DuplicateUserError(Exception):
    """Raised when a username or email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when a login attempt fails."""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    salt_hex, _, _ = stored.partition("$")
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
        raise DuplicateUserError("That username or email is already registered.") from e
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> sqlite3.Row:
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
        raise DuplicateUserError("That email is already registered.") from e
    finally:
        conn.close()


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


def upsert_goal(
    user_id: int,
    goal_type: str,
    target_value: float,
    start_value: float | None,
    start_date: str,
    target_date: str | None,
) -> None:
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
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM Goal WHERE user_id = ?", (user_id,)).fetchall()
        return {row["goal_type"]: row for row in rows}
    finally:
        conn.close()


def get_latest_weight(user_id: int) -> float | None:
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
    """Aggregate today's totals for the Progress Tracker page."""
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
