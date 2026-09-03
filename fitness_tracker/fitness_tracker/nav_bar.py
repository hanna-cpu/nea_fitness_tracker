"""Shared nav bar component - not a page itself, so no _state.py; it only
reads/calls the shared app_state.State (logout, username, notifications).
"""

import reflex as rx

from .app_state import State

NAV_LINKS = [
    ("Home", "/home", "house"),
    ("Account Settings", "/account-settings", "settings"),
    ("Add Fitness Data", "/add-fitness-data", "dumbbell"),
    ("Fitness Goals", "/fitness-goals", "target"),
    ("History", "/history", "history"),
]


def _notification_row(notification: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.icon("bell", size=14, color="var(--amber-9)", flex_shrink="0"),
        rx.text(notification["message"], size="2"),
        rx.spacer(),
        rx.icon_button(
            rx.icon("x", size=12),
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
    return rx.popover.root(
        rx.popover.trigger(
            rx.icon_button(
                rx.icon("bell", size=18),
                variant="soft",
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
        rx.link(
            rx.hstack(
                rx.icon("activity", size=22, color="var(--violet-9)"),
                rx.heading("Fitness Tracker", size="5", color_scheme="violet"),
                spacing="2",
                align="center",
            ),
            href="/home",
        ),
        rx.spacer(),
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
        rx.color_mode.button(),
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
