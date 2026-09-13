"""Backend logic for the Register page (register_page.py)."""

import reflex as rx

from . import db
from .app_state import State


class RegisterState(State):
    # One variable per form field, all prefixed reg_ so they can't clash
    # with the plain "username" field on the shared State.
    reg_name: str = ""
    reg_username: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_date_of_birth: str = ""
    error: str = ""

    def set_reg_name(self, value: str):
        self.reg_name = value

    def set_reg_username(self, value: str):
        self.reg_username = value

    def set_reg_email(self, value: str):
        self.reg_email = value

    def set_reg_password(self, value: str):
        self.reg_password = value

    def set_reg_date_of_birth(self, value: str):
        self.reg_date_of_birth = value

    def check_already_logged_in(self):
        """If someone who's already logged in opens the Register page, there's
        nothing for them to do here - send them to Home instead.
        """
        if self.is_logged_in:
            return rx.redirect("/home")

    def handle_register(self):
        """Runs when the Register button is clicked."""
        self.error = ""
        # Basic validation - the mockup didn't include a Username/Password
        # field on the Register screen, but Login needs them, so they were
        # added here as required fields.
        if not (self.reg_name and self.reg_username and self.reg_email and self.reg_password):
            self.error = "Please fill in name, username, email and password."
            return

        try:
            user_id = db.create_user(
                username=self.reg_username,
                password=self.reg_password,
                email=self.reg_email,
                name=self.reg_name,
                date_of_birth=self.reg_date_of_birth or None,
            )
        except db.DuplicateUserError as e:
            self.error = str(e)
            return

        # Registration doubles as logging in - no need to make them log in
        # again straight after signing up.
        self.user_id = user_id
        self.username = self.reg_username
        self.reg_password = ""
        return rx.redirect("/home")
