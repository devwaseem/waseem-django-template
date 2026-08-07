{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
from __future__ import annotations

import re

import pytest
from django.core import mail
from django.test import Client, override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ninja.errors import HttpError

from {{ cookiecutter.project_slug }}.api import auth
from {{ cookiecutter.project_slug }}.api.router import (
    authentication_error,
    http_error,
    not_found,
    unhandled_error,
    validation_error,
)
from {{ cookiecutter.project_slug }}.platform.models import User


REGISTER = "/api/v1/auth/register"
TOKEN = "/api/v1/auth/token"
REFRESH = "/api/v1/auth/token/refresh"
REVOKE = "/api/v1/auth/token/revoke"
ME = "/api/v1/auth/me"
RESET = "/api/v1/auth/password/reset"
RESET_CONFIRM = "/api/v1/auth/password/reset/confirm"
PASSWORD = "Correct-horse-battery-1"


def post(client: Client, path: str, payload: dict[str, str]):
    return client.post(path, data=payload, content_type="application/json")


@pytest.mark.django_db
def test_registration_and_jwt_lifecycle(client: Client) -> None:
    registered = post(
        client, REGISTER, {"email": "Person@Example.Test", "password": PASSWORD}
    )
    assert registered.status_code == 201
    assert registered.json()["email"] == "person@example.test"
    duplicate = post(
        client, REGISTER, {"email": "PERSON@example.test", "password": PASSWORD}
    )
    assert duplicate.status_code == 409
    assert duplicate["Content-Type"].startswith("application/problem+json")
    assert duplicate.json()["request_id"] == duplicate["X-Request-ID"]

    denied = post(client, TOKEN, {"email": "person@example.test", "password": "wrong"})
    assert denied.status_code == 401
    tokens = post(client, TOKEN, {"email": "person@example.test", "password": PASSWORD})
    assert tokens.status_code == 200
    access, refresh = tokens.json()["access"], tokens.json()["refresh"]
    assert client.get(ME).status_code == 401
    assert (
        client.get(ME, HTTP_AUTHORIZATION=f"Bearer {access}").json()["email"]
        == "person@example.test"
    )

    rotated = post(client, REFRESH, {"refresh": refresh})
    assert rotated.status_code == 200
    assert post(client, REFRESH, {"refresh": refresh}).status_code == 401
    assert (
        post(client, REVOKE, {"refresh": rotated.json()["refresh"]}).status_code == 204
    )
    assert post(client, REVOKE, {"refresh": "not-a-token"}).status_code == 401


@pytest.mark.django_db
def test_registration_toggle_and_password_reset_flow(client: Client) -> None:
    with override_settings(ACCOUNT_ALLOW_REGISTRATION=False):
        assert (
            post(
                client, REGISTER, {"email": "nope@example.test", "password": PASSWORD}
            ).status_code
            == 403
        )

    user = User.objects.create_user("reset@example.test", PASSWORD)
    assert post(client, RESET, {"email": "unknown@example.test"}).status_code == 202
    assert len(mail.outbox) == 0
    assert post(client, RESET, {"email": user.email}).status_code == 202
    assert len(mail.outbox) == 1
    url = re.search(r"http://testserver(?P<path>\S+)", mail.outbox[0].body)
    assert url is not None
    query = url.group("path").split("?", maxsplit=1)[1]
    values = dict(item.split("=", maxsplit=1) for item in query.split("&"))
    assert (
        post(
            client,
            RESET_CONFIRM,
            {
                "uid": values["uid"],
                "token": values["token"],
                "password": "New-correct-password-2",
            },
        ).status_code
        == 204
    )
    assert (
        post(
            client, TOKEN, {"email": user.email, "password": "New-correct-password-2"}
        ).status_code
        == 200
    )
    assert (
        post(
            client, RESET_CONFIRM, {"uid": "bad", "token": "bad", "password": PASSWORD}
        ).status_code
        == 400
    )


@pytest.mark.django_db
def test_auth_helpers_and_uniform_error_handlers(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    user = User.objects.create_user("helper@example.test", PASSWORD)
    assert auth.serialize_user(user).email == user.email
    pair = auth.token_pair_for(user)
    assert (
        auth.bearer_auth.authenticate(client.get(ME).wsgi_request, pair.access) == user
    )
    assert auth.bearer_auth.authenticate(client.get(ME).wsgi_request, "bad") is None
    request = client.get(ME).wsgi_request
    assert (
        auth.problem(
            request, status=418, code="teapot", title="Teapot", detail="Short"
        ).status_code
        == 418
    )

    from ninja.errors import AuthenticationError, ValidationError
    from django.http import Http404

    assert authentication_error(request, AuthenticationError()).status_code == 401
    assert validation_error(request, ValidationError([])).status_code == 422
    assert http_error(request, HttpError(400, "no")).status_code == 400
    assert not_found(request, Http404()).status_code == 404
    monkeypatch.setattr(
        "{{ cookiecutter.project_slug }}.api.router.logger.exception",
        lambda *_args, **_kwargs: None,
    )
    assert unhandled_error(request, RuntimeError("hidden")).status_code == 500

    encoded = urlsafe_base64_encode(force_bytes(user.pk))
    assert encoded
{% endif -%}
