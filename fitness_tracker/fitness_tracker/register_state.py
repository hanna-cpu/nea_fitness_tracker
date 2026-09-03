import reflex as rx

from . import db
from .app_state import State


class RegisterState(State):
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
        if self.is_logged_in:
            return rx.redirect("/home")

    def handle_register(self):
        self.error = ""
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

        self.user_id = user_id
        self.username = self.reg_username
        self.reg_password = ""
        return rx.redirect("/home")
