"""Shared session state.

In Reflex, a "State" class holds the data a page's UI reacts to, plus the
functions ("event handlers") that change that data - e.g. clicking a button
calls a function here, which updates a variable here, which the page
re-renders to match.

Every page-specific *_state.py class inherits from this State class, so
things that ALL pages need (whether someone is logged in, who they are, and
their unread notifications) live in one place instead of being copied into
every page's own state. This is the one deliberate exception to the
"one page = one *_page.py + one *_state.py" rule: session-wide data isn't
tied to a single page, so it lives here instead.
"""

from datetime import date

import reflex as rx

from . import db


class State(rx.State):
    # 0 means "nobody is logged in" - checked as user_id > 0 wherever it matters.
    user_id: int = 0
    name: str = ""
    # Unread notifications for the bell icon in the nav bar, e.g.
    # [{"id": 3, "message": "You haven't logged any activity today..."}]
    notifications: list[dict] = []

    def refresh_notifications(self):
        """Re-check for a "you haven't logged anything today" reminder and reload
        the unread notifications list. Called every time a logged-in page loads,
        so the bell icon is always up to date no matter which page you land on.
        """
        if self.user_id <= 0:
            return
        db.ensure_daily_activity_reminder(self.user_id, date.today().isoformat())
        self.notifications = [
            {"id": row["notification_id"], "message": row["message"]}
            for row in db.get_unread_notifications(self.user_id)
        ]

    def dismiss_notification(self, notification_id: int):
        """Mark one notification as read and remove it from the list shown on screen."""
        db.mark_notification_read(notification_id)
        self.notifications = [n for n in self.notifications if n["id"] != notification_id]

    def logout(self):
        """Clear the session and send the user back to the Login page."""
        self.user_id = 0
        self.name = ""
        self.notifications = []
        return rx.redirect("/login")
