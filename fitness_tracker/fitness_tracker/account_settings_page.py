import reflex as rx

from .account_settings_state import AccountSettingsState


def account_settings() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("Account Settings", size="7", color_scheme="blue"),
                rx.spacer(),
                rx.link("Back to Home", href="/home", color_scheme="blue"),
                width="100%",
                align="center",
            ),
            rx.cond(
                AccountSettingsState.error != "",
                rx.callout(AccountSettingsState.error, color_scheme="red", width="100%"),
            ),
            rx.cond(
                AccountSettingsState.message != "",
                rx.callout(AccountSettingsState.message, color_scheme="green", width="100%"),
            ),
            rx.vstack(
                rx.text("Name", size="2", color="gray"),
                rx.input(
                    value=AccountSettingsState.name,
                    on_change=AccountSettingsState.set_name,
                    width="100%",
                    size="3",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.vstack(
                rx.text("Email", size="2", color="gray"),
                rx.input(
                    type="email",
                    value=AccountSettingsState.email,
                    on_change=AccountSettingsState.set_email,
                    width="100%",
                    size="3",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.vstack(
                rx.text("Gender", size="2", color="gray"),
                rx.select(
                    ["Male", "Female", "Other"],
                    value=AccountSettingsState.gender,
                    on_change=AccountSettingsState.set_gender,
                    placeholder="Select gender",
                    width="100%",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.vstack(
                rx.text("Height (cm)", size="2", color="gray"),
                rx.input(
                    type="number",
                    value=AccountSettingsState.height_cm,
                    on_change=AccountSettingsState.set_height_cm,
                    width="100%",
                    size="3",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.vstack(
                rx.text("Date of Birth", size="2", color="gray"),
                rx.input(
                    type="date",
                    value=AccountSettingsState.date_of_birth,
                    on_change=AccountSettingsState.set_date_of_birth,
                    width="100%",
                    size="3",
                ),
                spacing="1",
                width="100%",
                align="start",
            ),
            rx.button(
                "Save",
                on_click=AccountSettingsState.save,
                width="100%",
                size="3",
                color_scheme="blue",
            ),
            spacing="4",
            width="26em",
            padding="2em",
            border="1px solid var(--gray-6)",
            border_radius="var(--radius-4)",
        ),
        padding="2em",
    )
