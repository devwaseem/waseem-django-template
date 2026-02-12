from typing import Any

from allauth.account.views import LoginView
from allauth.account.views import PasswordResetDoneView
from allauth.account.views import PasswordResetFromKeyDoneView
from allauth.account.views import PasswordResetFromKeyView
from allauth.account.views import PasswordResetView
from allauth.account.views import SignupView
from django.http import HttpResponse

from frontend.pages.auth.login import LoginPage
from frontend.pages.auth.password_reset import PasswordResetPage
from frontend.pages.auth.password_reset_done import PasswordResetDonePage
from frontend.pages.auth.password_reset_from_key import (
    PasswordResetFromKeyPage,
)
from frontend.pages.auth.password_reset_from_key_done import (
    PasswordResetFromKeyDonePage,
)
from frontend.pages.auth.signup import SignupPage


class AccountLoginView(LoginView):
    template_name = "pages/auth/login/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return LoginPage(context=context).as_response(request=self.request)


class AccountSignupView(SignupView):
    template_name = "pages/auth/signup/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return SignupPage(context=context).as_response(request=self.request)


class AccountResetPasswordView(PasswordResetView):
    template_name = "pages/auth/password_reset/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return PasswordResetPage(context=context).as_response(
            request=self.request
        )


class AccountResetPasswordDoneView(PasswordResetDoneView):
    template_name = "pages/auth/password_reset_done/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return PasswordResetDonePage(context=context).as_response(
            request=self.request
        )


class AccountResetPasswordFromKeyView(PasswordResetFromKeyView):
    template_name = "pages/auth/password_reset_from_key/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return PasswordResetFromKeyPage(context=context).as_response(
            request=self.request
        )


class AccountResetPasswordFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = "pages/auth/password_reset_from_key_done/index.html"

    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse:
        return PasswordResetFromKeyDonePage(context=context).as_response(
            request=self.request
        )
