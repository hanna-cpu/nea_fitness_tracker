"""Shared session state. Every page-specific *_state.py inherits from this
State so login status is available everywhere, instead of duplicating it
per page.
"""

import reflex as rx


class State(rx.State):
    user_id: int = 0
    username: str = ""

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user_id > 0

    def logout(self):
        self.user_id = 0
        self.username = ""
        return rx.redirect("/login")
