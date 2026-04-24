from __future__ import annotations

from django.urls import resolve, reverse


def test_auth_routes_resolve_to_custom_views() -> None:
    """Auth routes use custom HyperDjango account views."""
    cases = [
        ("account_login", reverse("account_login")),
        ("account_logout", reverse("account_logout")),
        ("account_signup", reverse("account_signup")),
        ("account_reset_password", reverse("account_reset_password")),
        (
            "account_reset_password_done",
            reverse("account_reset_password_done"),
        ),
        (
            "account_reset_password_from_key",
            reverse(
                "account_reset_password_from_key",
                kwargs={"uidb36": "abc", "key": "token"},
            ),
        ),
        (
            "account_reset_password_from_key_done",
            reverse("account_reset_password_from_key_done"),
        ),
    ]

    for route_name, path in cases:
        match = resolve(path)
        assert match.view_name == route_name
