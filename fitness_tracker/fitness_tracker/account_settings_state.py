import reflex as rx

from . import db
from .app_state import State


class AccountSettingsState(State):
    name: str = ""
    email: str = ""
    gender: str = ""
    height_cm: str = ""
    date_of_birth: str = ""
    message: str = ""
    error: str = ""

    def set_name(self, value: str):
        self.name = value

    def set_email(self, value: str):
        self.email = value

    def set_gender(self, value: str):
        self.gender = value

    def set_height_cm(self, value: str):
        self.height_cm = value

    def set_date_of_birth(self, value: str):
        self.date_of_birth = value

    def load_user(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
        user = db.get_user(self.user_id)
        if user is None:
            return
        self.name = user["name"] or ""
        self.email = user["email"] or ""
        self.gender = user["gender"] or ""
        self.height_cm = str(user["height_cm"]) if user["height_cm"] is not None else ""
        self.date_of_birth = user["date_of_birth"] or ""

    def save(self):
        self.message = ""
        self.error = ""
        if not (self.name and self.email):
            self.error = "Name and email are required."
            return

        height_value = None
        if self.height_cm:
            try:
                height_value = float(self.height_cm)
            except ValueError:
                self.error = "Height must be a number."
                return

        try:
            db.update_user(
                user_id=self.user_id,
                name=self.name,
                email=self.email,
                gender=self.gender or None,
                height_cm=height_value,
                date_of_birth=self.date_of_birth or None,
            )
        except db.DuplicateUserError as e:
            self.error = str(e)
            return

        self.message = "Saved."
