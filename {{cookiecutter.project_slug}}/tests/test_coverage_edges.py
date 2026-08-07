from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from unittest.mock import Mock

import pytest
from django.conf import settings
from django.test import Client
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from {{ cookiecutter.project_slug }}.config.env import Environment
from {{ cookiecutter.project_slug }}.domains.registry import extra_urlpatterns
from {{ cookiecutter.project_slug }}.platform.models import User


def test_environment_handles_boolean_and_iterable_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    environment = Environment()
    monkeypatch.setattr(environment, "_raw", lambda *_args, **_kwargs: True)
    assert environment.boolean("ANY") is True
    monkeypatch.setattr(environment, "_raw", lambda *_args, **_kwargs: ("one", " two "))
    assert environment.list("ANY") == ["one", "two"]


def test_domain_extension_points_are_explicit_noops() -> None:
    assert extra_urlpatterns() == ()
    project_package = settings.ROOT_URLCONF.partition(".")[0]
    domain_registry = import_module(f"{project_package}.domains.registry")
    register_api = getattr(domain_registry, "register_api", None)
    if register_api is not None:
        assert register_api(object()) is None

    celery_module_name = f"{project_package}.platform.celery"
    if find_spec(celery_module_name) is not None:
        celery = import_module(celery_module_name)
        assert celery.app.main == project_package


@pytest.mark.django_db
def test_remaining_platform_and_api_error_paths(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(ValueError, match="is_superuser"):
        User.objects.create_superuser(
            "not-admin@example.test", "Correct-horse-battery-1", is_superuser=False
        )

    from {{ cookiecutter.project_slug }}.platform import health

    monkeypatch.setattr(health.cache, "set", Mock())
    monkeypatch.setattr(health.cache, "get", lambda *_args, **_kwargs: "missing")
    assert client.get("/readyz/").status_code == 503

    if settings.RENDERING_MODE == "ssr":
        return

    user = User.objects.create_user(
        "validation@example.test", "Correct-horse-battery-1"
    )
    assert (
        client.post(
            "/api/v1/auth/register",
            data={"email": "short@example.test", "password": "short"},
            content_type="application/json",
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/v1/auth/password/reset/confirm",
            data={
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": __import__(
                    "django.contrib.auth.tokens", fromlist=["default_token_generator"]
                ).default_token_generator.make_token(user),
                "password": "short",
            },
            content_type="application/json",
        ).status_code
        == 422
    )
