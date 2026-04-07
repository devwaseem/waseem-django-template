from __future__ import annotations

from django.urls import resolve, reverse

from hyper.routes.account.login.page import PageView as AccountLoginPageView
from hyper.routes.account.logout.page import PageView as AccountLogoutPageView
from hyper.routes.account.password.reset.page import (
    PageView as AccountResetPasswordPageView,
)
from hyper.routes.account.password.reset_done.page import (
    PageView as AccountResetPasswordDonePageView,
)
from hyper.routes.account.password.reset_key.page import (
    PageView as AccountResetPasswordFromKeyPageView,
)
from hyper.routes.account.password.reset_key_done.page import (
    PageView as AccountResetPasswordFromKeyDonePageView,
)
from hyper.routes.account.register.page import (
    PageView as AccountSignupPageView,
)


def test_auth_routes_resolve_to_custom_views() -> None:
    """Auth routes use custom HyperDjango account views."""
    cases = [
        ("account_login", reverse("account_login"), AccountLoginPageView),
        ("account_logout", reverse("account_logout"), AccountLogoutPageView),
        ("account_signup", reverse("account_signup"), AccountSignupPageView),
        (
            "account_reset_password",
            reverse("account_reset_password"),
            AccountResetPasswordPageView,
        ),
        (
            "account_reset_password_done",
            reverse("account_reset_password_done"),
            AccountResetPasswordDonePageView,
        ),
        (
            "account_reset_password_from_key",
            reverse(
                "account_reset_password_from_key",
                kwargs={"uidb36": "abc", "key": "token"},
            ),
            AccountResetPasswordFromKeyPageView,
        ),
        (
            "account_reset_password_from_key_done",
            reverse("account_reset_password_from_key_done"),
            AccountResetPasswordFromKeyDonePageView,
        ),
    ]

    for route_name, path, view_class in cases:
        match = resolve(path)
        assert match.view_name == route_name
        assert getattr(match.func, "view_class", None) is view_class
