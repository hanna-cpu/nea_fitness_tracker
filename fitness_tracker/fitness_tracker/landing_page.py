"""No landing_state.py: this page is static and has no backend logic."""

import reflex as rx


def landing() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Fitness Tracker", size="9", color_scheme="violet"),
            rx.text(
                "Log workouts, weight, calories and steps in one place. "
                "Set goals, track your progress, and stay on top of your fitness.",
                size="4",
                color="gray",
                text_align="center",
                max_width="32em",
            ),
            rx.hstack(
                rx.link(
                    rx.button("Login", size="4", color_scheme="violet"),
                    href="/login",
                ),
                rx.link(
                    rx.button("Register", size="4", variant="outline", color_scheme="violet"),
                    href="/register",
                ),
                spacing="4",
            ),
            spacing="6",
            align="center",
        ),
        height="100vh",
        padding="2em",
        background="linear-gradient(135deg, var(--blue-3), var(--purple-3))",
    )
