"""Backend logic for the Register page (register_page.py)."""

import reflex as rx
from . import db
from .app_state import State
class RegisterState(State):
    reg_name: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_date_of_birth: str = ""
    error: str = ""

    def set_reg_name(self, value: str):
        self.reg_name = value

    def set_reg_email(self, value: str):
        self.reg_email = value

    def set_reg_password(self, value: str):
        self.reg_password = value

    def set_reg_date_of_birth(self, value: str):
        self.reg_date_of_birth = value

    def check_already_logged_in(self):
        """If someone who's already logged in opens the Register page, 
        send them to Home instead.
        """
        if self.user_id > 0:
            return rx.redirect("/home")

    def handle_register(self):
        """Runs when the Register button is clicked."""
        self.error = ""
        # Basic validation - make sure all fields are filled in.
        if not (self.reg_name and self.reg_email and self.reg_password):
            self.error = "Please fill in name, email and password."
            return
        try:
            user_id = db.create_user(
                password=self.reg_password,
                email=self.reg_email,
                name=self.reg_name,
                date_of_birth=self.reg_date_of_birth or None,
            )
        except db.DuplicateUserError as e:
            self.error = str(e)
            return

        # Registration successful, so set the user_id and name in the state so that the user is logged in
        self.user_id = user_id
        self.name = self.reg_name
        self.reg_password = ""
        return rx.redirect("/home")
