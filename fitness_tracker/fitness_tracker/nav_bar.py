"""Shared nav bar shown at the top of every logged-in page.

Not a page itself, so there's no matching nav_bar_state.py - it only reads
from and calls into the shared app_state.State (logout, username,
notifications), since navigation and notifications are the same everywhere.
"""

import reflex as rx

from .app_state import State

# (label shown to the user, URL it links to, lucide icon name)
NAV_LINKS = [
    ("Home", "/home", "house"),
    ("Account Settings", "/account-settings", "settings"),
    ("Add Fitness Data", "/add-fitness-data", "dumbbell"),
    ("Fitness Goals", "/fitness-goals", "target"),
    ("History", "/history", "history"),
]


def _notification_row(notification: rx.Var) -> rx.Component:
    """One line inside the notifications popover: the message plus a small X
    button to dismiss it. `notification` is a dict like {"id": 3, "message": "..."}.
    """
    return rx.hstack(
        rx.icon("bell", size=14, color="var(--amber-9)", flex_shrink="0"),
        rx.text(notification["message"], size="2"),
        rx.spacer(),
        rx.icon_button(
            rx.icon("x", size=12),
            # Calling dismiss_notification with the row's own id, so clicking
            # the X only dismisses THIS notification, not all of them.
            on_click=State.dismiss_notification(notification["id"]),
            variant="ghost",
            color_scheme="gray",
            size="1",
        ),
        width="100%",
        align="start",
        padding="0.5em 0",
        border_bottom="1px solid var(--gray-5)",
    )


def _notifications_popover() -> rx.Component:
    """The bell icon in the nav bar. Clicking it opens a small popup (a
    "popover") listing unread notifications, without leaving the page.
    """
    return rx.popover.root(
        rx.popover.trigger(
            rx.icon_button(
                rx.icon("bell", size=18),
                variant="soft",
                # rx.cond picks between the two colours depending on whether
                # there's anything unread - this is what turns the bell red.
                color_scheme=rx.cond(State.has_unread_notifications, "red", "gray"),
                radius="full",
                size="2",
            ),
        ),
        rx.popover.content(
            rx.vstack(
                rx.heading("Notifications", size="3"),
                rx.cond(
                    State.has_unread_notifications,
                    rx.vstack(
                        rx.foreach(State.notifications, _notification_row),
                        width="100%",
                        spacing="1",
                    ),
                    rx.text("No new notifications.", size="2", color="gray"),
                ),
                spacing="3",
                width="20em",
            ),
            side="bottom",
            align="end",
        ),
    )


def nav_bar() -> rx.Component:
    return rx.hstack(
        # App name/logo on the far left, also a link back to Home.
        rx.link(
            rx.hstack(
                rx.icon("activity", size=22, color="var(--violet-9)"),
                rx.heading("Fitness Tracker", size="5", color_scheme="violet"),
                spacing="2",
                align="center",
            ),
            href="/home",
        ),
        rx.spacer(),  # pushes everything after it to the right
        # One link per page, built from the NAV_LINKS list above.
        rx.hstack(
            *[
                rx.link(
                    rx.hstack(
                        rx.icon(icon, size=16),
                        rx.text(label),
                        spacing="1",
                        align="center",
                    ),
                    href=href,
                    color_scheme="violet",
                    weight="medium",
                )
                for label, href, icon in NAV_LINKS
            ],
            spacing="5",
        ),
        _notifications_popover(),
        rx.color_mode.button(),  # built-in light/dark mode toggle
        rx.button(
            rx.icon("log_out", size=16),
            "Logout",
            on_click=State.logout,
            variant="soft",
            color_scheme="gray",
            size="2",
        ),
        width="100%",
        padding="1em 2em",
        border_bottom="1px solid var(--gray-6)",
        align="center",
    )
