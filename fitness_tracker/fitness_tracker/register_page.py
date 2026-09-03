import reflex as rx

from .register_state import RegisterState


def register() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Register", size="7", color_scheme="violet"),
            rx.cond(
                RegisterState.error != "",
                rx.callout(
                    RegisterState.error,
                    color_scheme="red",
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="Name",
                value=RegisterState.reg_name,
                on_change=RegisterState.set_reg_name,
                width="100%",
                size="3",
            ),
            rx.input(
                placeholder="Username",
                value=RegisterState.reg_username,
                on_change=RegisterState.set_reg_username,
                width="100%",
                size="3",
            ),
            rx.input(
                placeholder="Email",
                type="email",
                value=RegisterState.reg_email,
                on_change=RegisterState.set_reg_email,
                width="100%",
                size="3",
            ),
            rx.input(
                placeholder="Password",
                type="password",
                value=RegisterState.reg_password,
                on_change=RegisterState.set_reg_password,
                width="100%",
                size="3",
            ),
            rx.vstack(
                rx.text("Date of Birth", size="2", color="gray"),
                rx.input(
                    type="date",
                    value=RegisterState.reg_date_of_birth,
                    on_change=RegisterState.set_reg_date_of_birth,
                    width="100%",
                    size="3",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.button(
                "Register",
                on_click=RegisterState.handle_register,
                width="100%",
                size="3",
                color_scheme="violet",
            ),
            rx.hstack(
                rx.text("Already have an account?", color="gray"),
                rx.link("Login", href="/login", color_scheme="violet", weight="bold"),
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
