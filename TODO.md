# TODO

Findings from reviewing the Reflex app (2026-09-08).

- [ ] Wire up `goal_achievement` notifications. The `Notification.type` CHECK
      constraint in `database/schema.sql` allows `'activity_reminder'` and
      `'goal_achievement'`, but `db.create_notification` is only ever called
      from `db.ensure_daily_activity_reminder`. No code path detects a user
      hitting a goal and creates a `goal_achievement` notification.
- [ ] Add basic validation in `fitness_tracker/register_state.py::handle_register`:
      email format check and a minimum password length/strength rule. Currently
      only checks that fields are non-empty.
- [ ] Reconcile run instructions with this environment. `docs/running-the-app.md`
      and `run_app.bat` assume Windows (`.venv\Scripts\activate.bat`, `winget`,
      Bun/Node workaround). Add a Linux/WSL equivalent (`source .venv/bin/activate`,
      `reflex run`) if the app needs to run here.
- [ ] `fitness_tracker/home_state.py::HomeState` defaults target vars (`steps_target`,
      `workout_target`, etc.) to `0` when no goal is set, so a new user's dashboard
      shows "0 / 0" instead of a clear empty state. Consider gating each card on
      whether the goal exists.
- [ ] (Low priority) `user_id` / `is_logged_in` on `app_state.State` are regular
      (client-visible) vars, so they show up in websocket traffic/devtools. Not
      exploitable since all mutations run server-side against the session's own
      state, but could be marked backend-only for strictness.
