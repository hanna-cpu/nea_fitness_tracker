-- Fitness Tracker database schema (SQLite)
-- Mirrors the "Database Design" tab in hierarchy diagram and UI.drawio

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS User (
    user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    date_of_birth   DATE,
    gender          TEXT,
    height_cm       REAL,
    profile_picture TEXT,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS WorkoutRecord (
    workout_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL,
    workout_type     TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    date             DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS WeightRecord (
    weight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    weight_kg REAL NOT NULL,
    date      DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CalorieRecord (
    calorie_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id            INTEGER NOT NULL,
    calories_consumed  INTEGER,
    calories_burned    INTEGER,
    date               DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StepRecord (
    step_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    step_count INTEGER NOT NULL,
    date       DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Goal (
    goal_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    goal_type    TEXT NOT NULL CHECK (goal_type IN ('steps', 'workout_duration', 'weight', 'calories')),
    target_value REAL NOT NULL,
    start_value  REAL,
    start_date   DATE NOT NULL,
    target_date  DATE,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL,
    type             TEXT NOT NULL CHECK (type IN ('activity_reminder', 'goal_achievement')),
    message          TEXT NOT NULL,
    date_created     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read          INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_workout_user ON WorkoutRecord (user_id);
CREATE INDEX IF NOT EXISTS idx_weight_user ON WeightRecord (user_id);
CREATE INDEX IF NOT EXISTS idx_calorie_user ON CalorieRecord (user_id);
CREATE INDEX IF NOT EXISTS idx_step_user ON StepRecord (user_id);
CREATE INDEX IF NOT EXISTS idx_goal_user ON Goal (user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_goal_user_type ON Goal (user_id, goal_type);
CREATE INDEX IF NOT EXISTS idx_notification_user ON Notification (user_id);
