import reflex as rx

from .app_state import State


def _nav_button(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.button(label, width="100%", size="4", color_scheme="blue"),
        href=href,
        width="100%",
    )


def home() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Welcome back", size="7", color_scheme="blue"),
            rx.text(State.username, size="5", weight="bold"),
            rx.grid(
                _nav_button("Account Settings", "/account-settings"),
                _nav_button("Add Fitness Data", "/add-fitness-data"),
                _nav_button("Progress Tracker", "/progress-tracker"),
                _nav_button("Fitness Goals", "/fitness-goals"),
                _nav_button("History", "/history"),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.button(
                "Logout",
                on_click=State.logout,
                variant="soft",
                color_scheme="gray",
                margin_top="2em",
            ),
            spacing="6",
            width="32em",
            padding="2em",
        ),
        height="100vh",
    )
