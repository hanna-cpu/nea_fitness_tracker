"""Backend logic for the Login page (login_page.py)."""

import reflex as rx

from . import db
from .app_state import State


class LoginState(State):
    # These hold whatever the user has typed into the two input boxes.
    login_username: str = ""
    login_password: str = ""
    # Shown as a red error message when a login attempt fails.
    error: str = ""

    # Reflex used to auto-generate these "set_<var>" functions for every
    # variable, but that's been switched off in this version - so each input
    # box needs its own tiny function to update its variable when typed in.
    def set_login_username(self, value: str):
        self.login_username = value

    def set_login_password(self, value: str):
        self.login_password = value

    def check_already_logged_in(self):
        """Runs when the Login page loads. If the user is already logged in,
        there's no reason to show them the login form again - send them
        straight to Home instead.
        """
        if self.is_logged_in:
            return rx.redirect("/home")

    def handle_login(self):
        """Runs when the Login button is clicked."""
        self.error = ""
        try:
            user = db.authenticate_user(self.login_username, self.login_password)
        except db.InvalidCredentialsError as e:
            self.error = str(e)
            return

        # Success: store who's logged in (in the shared State, so every page
        # can see it) and clear the password from memory before leaving.
        self.user_id = user["user_id"]
        self.username = user["username"]
        self.login_password = ""
        return rx.redirect("/home")
