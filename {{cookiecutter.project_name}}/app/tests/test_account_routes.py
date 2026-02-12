from __future__ import annotations

from django.urls import resolve
from django.urls import reverse

from app.account.views import AccountLoginView
from app.account.views import AccountResetPasswordDoneView
from app.account.views import AccountResetPasswordFromKeyDoneView
from app.account.views import AccountResetPasswordFromKeyView
from app.account.views import AccountResetPasswordView
from app.account.views import AccountSignupView


def test_auth_routes_resolve_to_custom_views() -> None:
    """Auth routes use custom frontend-kit account views."""
    cases = [
        ("account_login", reverse("account_login"), AccountLoginView),
        ("account_signup", reverse("account_signup"), AccountSignupView),
        (
            "account_reset_password",
            reverse("account_reset_password"),
            AccountResetPasswordView,
        ),
        (
            "account_reset_password_done",
            reverse("account_reset_password_done"),
            AccountResetPasswordDoneView,
        ),
        (
            "account_reset_password_from_key",
            reverse(
                "account_reset_password_from_key",
                kwargs={"uidb36": "abc", "key": "token"},
            ),
            AccountResetPasswordFromKeyView,
        ),
        (
            "account_reset_password_from_key_done",
            reverse("account_reset_password_from_key_done"),
            AccountResetPasswordFromKeyDoneView,
        ),
    ]

    for route_name, route_path, view_class in cases:
        match = resolve(route_path)
        assert match.view_name == route_name
        assert match.func.view_class is view_class
