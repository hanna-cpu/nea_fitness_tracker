"""Shared session state. Every page-specific *_state.py inherits from this
State so login status and notifications are available everywhere, instead of
duplicating them per page.
"""

from datetime import date

import reflex as rx

from . import db


class State(rx.State):
    user_id: int = 0
    username: str = ""
    notifications: list[dict] = []

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user_id > 0

    @rx.var
    def has_unread_notifications(self) -> bool:
        return len(self.notifications) > 0

    def refresh_notifications(self):
        if not self.is_logged_in:
            return
        db.ensure_daily_activity_reminder(self.user_id, date.today().isoformat())
        self.notifications = [
            {"id": row["notification_id"], "message": row["message"]}
            for row in db.get_unread_notifications(self.user_id)
        ]

    def dismiss_notification(self, notification_id: int):
        db.mark_notification_read(notification_id)
        self.notifications = [n for n in self.notifications if n["id"] != notification_id]

    def logout(self):
        self.user_id = 0
        self.username = ""
        self.notifications = []
        return rx.redirect("/login")
