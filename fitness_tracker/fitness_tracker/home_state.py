import reflex as rx

from .app_state import State


class HomeState(State):
    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
