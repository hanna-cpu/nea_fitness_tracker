import reflex as rx

from . import db
from .app_state import State


class LoginState(State):
    login_username: str = ""
    login_password: str = ""
    error: str = ""

    def set_login_username(self, value: str):
        self.login_username = value

    def set_login_password(self, value: str):
        self.login_password = value

    def check_already_logged_in(self):
        if self.is_logged_in:
            return rx.redirect("/home")

    def handle_login(self):
        self.error = ""
        try:
            user = db.authenticate_user(self.login_username, self.login_password)
        except db.InvalidCredentialsError as e:
            self.error = str(e)
            return

        self.user_id = user["user_id"]
        self.username = user["username"]
        self.login_password = ""
        return rx.redirect("/home")
