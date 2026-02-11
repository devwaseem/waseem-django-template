from allauth.account.forms import LoginForm

from frontend.layouts.base import BaseLayout


class LoginPage(BaseLayout):
    def __init__(self, form: LoginForm, next_url: str = "") -> None:
        super().__init__(title="Login")
        self.form = form
        self.next_url = next_url
