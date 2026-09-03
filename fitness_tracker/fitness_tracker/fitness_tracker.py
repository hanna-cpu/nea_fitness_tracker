import reflex as rx

from .account_settings_page import account_settings
from .account_settings_state import AccountSettingsState
from .add_fitness_data_page import add_fitness_data
from .add_fitness_data_state import AddFitnessDataState
from .fitness_goals_page import fitness_goals
from .fitness_goals_state import FitnessGoalsState
from .history_page import history
from .history_state import HistoryState
from .home_page import home
from .home_state import HomeState
from .landing_page import landing
from .login_page import login
from .login_state import LoginState
from .register_page import register
from .register_state import RegisterState
from .app_state import State

app = rx.App(
    theme=rx.theme(
        accent_color="violet",
        gray_color="slate",
        radius="large",
    )
)

app.add_page(landing, route="/")
app.add_page(login, route="/login", on_load=LoginState.check_already_logged_in)
app.add_page(register, route="/register", on_load=RegisterState.check_already_logged_in)
app.add_page(home, route="/home", on_load=HomeState.load_home)
app.add_page(
    account_settings,
    route="/account-settings",
    on_load=[AccountSettingsState.load_user, State.refresh_notifications],
)
app.add_page(
    add_fitness_data,
    route="/add-fitness-data",
    on_load=[AddFitnessDataState.load_defaults, State.refresh_notifications],
)
app.add_page(
    fitness_goals,
    route="/fitness-goals",
    on_load=[FitnessGoalsState.load_goals, State.refresh_notifications],
)
app.add_page(
    history,
    route="/history",
    on_load=[HistoryState.load_history, State.refresh_notifications],
)
