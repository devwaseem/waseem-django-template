"""Rate-limit policy and transport integration tests."""

from __future__ import annotations

from importlib import import_module

import pytest
from django.core.cache import cache
from django.test import Client, RequestFactory, override_settings

{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
from {{ cookiecutter.project_slug }}.api.auth import token_pair_for
from {{ cookiecutter.project_slug }}.platform.models import User
{% endif -%}
from {{ cookiecutter.project_slug }}.platform.ratelimits import (
    RateLimitExceeded,
    enforce_public_auth_rate_limits,
    enforce_rate_limit,
)


@pytest.fixture(autouse=True)
def clear_rate_limit_cache() -> None:
    """Keep request counters isolated between contract tests."""
    cache.clear()
    yield
    cache.clear()


def test_rate_limit_allows_under_limit_requests(
    monkeypatch: pytest.MonkeyPatch, rf: RequestFactory
) -> None:
    rate_limits = import_module("{{ cookiecutter.project_slug }}.platform.ratelimits")
    monkeypatch.setattr(rate_limits, "get_usage", lambda _request, **_kwargs: None)

    enforce_rate_limit(rf.get("/"), group="test", key="ip", rate="1/m")


def test_rate_limit_blocks_requests_with_a_retry_header_value(
    monkeypatch: pytest.MonkeyPatch, rf: RequestFactory
) -> None:
    rate_limits = import_module("{{ cookiecutter.project_slug }}.platform.ratelimits")
    monkeypatch.setattr(
        rate_limits,
        "get_usage",
        lambda _request, **_kwargs: {"should_limit": True, "time_left": 0.1},
    )

    with pytest.raises(RateLimitExceeded) as error:
        enforce_rate_limit(rf.get("/"), group="test", key="ip", rate="1/m")

    assert error.value.retry_after == 1


@pytest.mark.parametrize(
    ("action", "email", "expected_settings"),
    [
        (
            "login",
            "Person@Example.Test ",
            ("RATE_LIMIT_LOGIN_IP", "RATE_LIMIT_LOGIN_ACCOUNT"),
        ),
        (
            "registration",
            "Person@Example.Test ",
            ("RATE_LIMIT_REGISTRATION_IP", "RATE_LIMIT_REGISTRATION_ACCOUNT"),
        ),
        (
            "password_reset",
            "Person@Example.Test ",
            ("RATE_LIMIT_PASSWORD_RESET_IP", "RATE_LIMIT_PASSWORD_RESET_ACCOUNT"),
        ),
    ],
)
def test_public_auth_limits_use_independent_ip_and_account_counters(
    action: str,
    email: str,
    expected_settings: tuple[str, str],
    monkeypatch: pytest.MonkeyPatch,
    rf: RequestFactory,
) -> None:
    rate_limits = import_module("{{ cookiecutter.project_slug }}.platform.ratelimits")
    calls: list[tuple[str, object, str]] = []

    def record_rate_limit(
        _request: object, *, group: str, key: object, rate: str
    ) -> None:
        calls.append((group, key, rate))

    monkeypatch.setattr(rate_limits, "enforce_rate_limit", record_rate_limit)

    enforce_public_auth_rate_limits(
        rf.post("/", {"email": email}), action=action, email=email
    )

    assert calls[0] == (
        f"public-auth:{action}:ip",
        "ip",
        getattr(rate_limits.settings, expected_settings[0]),
    )
    assert calls[1][0] == f"public-auth:{action}:account"
    assert calls[1][2] == getattr(rate_limits.settings, expected_settings[1])
    assert calls[1][1]("ignored", rf.get("/")) == "person@example.test"


{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
@pytest.mark.django_db
def test_api_limit_returns_an_rfc_9457_problem_with_retry_after(client: Client) -> None:
    user = User.objects.create_user("rate-limit@example.test", "Correct-horse-battery-1")
    access = token_pair_for(user).access
    with override_settings(RATELIMIT_ENABLE=True, RATE_LIMIT_API_IP="1/h"):
        assert client.get(
            "/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {access}"
        ).status_code == 200
        response = client.get("/api/v1/auth/me", HTTP_AUTHORIZATION=f"Bearer {access}")

    assert response.status_code == 429
    assert response["Content-Type"].startswith("application/problem+json")
    assert response["Retry-After"]
    assert response.json()["code"] == "rate_limited"


@pytest.mark.django_db
def test_login_limit_combines_ip_and_account_counters(client: Client) -> None:
    with override_settings(
        RATELIMIT_ENABLE=True,
        RATE_LIMIT_API_IP="100/h",
        RATE_LIMIT_LOGIN_IP="1/h",
        RATE_LIMIT_LOGIN_ACCOUNT="100/h",
    ):
        first = client.post(
            "/api/v1/auth/token",
            data={"email": "first@example.test", "password": "wrong"},
            content_type="application/json",
        )
        response = client.post(
            "/api/v1/auth/token",
            data={"email": "second@example.test", "password": "wrong"},
            content_type="application/json",
        )

    assert first.status_code == 401
    assert response.status_code == 429
    assert response.json()["code"] == "rate_limited"
{% endif -%}


{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
@pytest.mark.django_db
def test_ssr_auth_posts_use_the_shared_rate_limit_policy(client: Client) -> None:
    with override_settings(
        RATELIMIT_ENABLE=True,
        RATE_LIMIT_LOGIN_IP="100/h",
        RATE_LIMIT_LOGIN_ACCOUNT="100/h",
        RATE_LIMIT_REGISTRATION_IP="100/h",
        RATE_LIMIT_REGISTRATION_ACCOUNT="100/h",
        RATE_LIMIT_PASSWORD_RESET_IP="100/h",  # noqa: S106 - test rate setting.
        RATE_LIMIT_PASSWORD_RESET_ACCOUNT="100/h",  # noqa: S106 - test rate setting.
    ):
        assert (
            client.post("/login/", {"login": "person@example.test"}).status_code == 200
        )
        assert (
            client.post("/register/", {"email": "new@example.test"}).status_code == 200
        )
        assert (
            client.post("/password/reset/", {"email": "reset@example.test"}).status_code
            == 302
        )
{% endif -%}
