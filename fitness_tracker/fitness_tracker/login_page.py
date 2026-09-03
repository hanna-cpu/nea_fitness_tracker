import reflex as rx

from .login_state import LoginState


def login() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Login", size="7", color_scheme="violet"),
            rx.cond(
                LoginState.error != "",
                rx.callout(
                    LoginState.error,
                    color_scheme="red",
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="Username",
                value=LoginState.login_username,
                on_change=LoginState.set_login_username,
                width="100%",
                size="3",
            ),
            rx.input(
                placeholder="Password",
                type="password",
                value=LoginState.login_password,
                on_change=LoginState.set_login_password,
                width="100%",
                size="3",
            ),
            rx.button(
                "Login",
                on_click=LoginState.handle_login,
                width="100%",
                size="3",
                color_scheme="violet",
            ),
            rx.hstack(
                rx.text("Don't have an account?", color="gray"),
                rx.link("Sign Up", href="/register", color_scheme="violet", weight="bold"),
                spacing="2",
            ),
            spacing="4",
            width="24em",
            padding="2em",
            background="var(--color-panel-solid)",
            border="1px solid var(--gray-6)",
            border_radius="var(--radius-4)",
        ),
        height="100vh",
        background="linear-gradient(135deg, var(--blue-3), var(--purple-3))",
    )
