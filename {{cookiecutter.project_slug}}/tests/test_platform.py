from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from io import StringIO
from pathlib import Path
from unittest.mock import Mock

import pytest
from django.conf import settings
from django.contrib.admin.sites import site
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client, RequestFactory, override_settings
from django_ratelimit.exceptions import Ratelimited

PROJECT_PACKAGE = settings.ROOT_URLCONF.partition(".")[0]
Environment = import_module(f"{PROJECT_PACKAGE}.config.env").Environment
UserAdmin = import_module(f"{PROJECT_PACKAGE}.platform.admin").UserAdmin
PlatformConfig = import_module(f"{PROJECT_PACKAGE}.platform.apps").PlatformConfig
account_settings = import_module(
    f"{PROJECT_PACKAGE}.platform.context_processors"
).account_settings
logging_module = import_module(f"{PROJECT_PACKAGE}.platform.logging")
REDACTED = logging_module.REDACTED
redact_sensitive_data = logging_module.redact_sensitive_data
models_module = import_module(f"{PROJECT_PACKAGE}.platform.models")
AdminImpersonationAuditEvent = models_module.AdminImpersonationAuditEvent
User = models_module.User
storage_module = import_module(f"{PROJECT_PACKAGE}.platform.storage")
PrivateMediaStorage = storage_module.PrivateMediaStorage
PublicStaticStorage = storage_module.PublicStaticStorage
tasks_module_name = f"{PROJECT_PACKAGE}.platform.tasks"
DomainTask = (
    import_module(tasks_module_name).DomainTask
    if find_spec(tasks_module_name) is not None
    else None
)
views_module = import_module(f"{PROJECT_PACKAGE}.platform.views")
handler403 = views_module.handler403
handler404 = views_module.handler404
handler500 = views_module.handler500
request_id_module = import_module(f"{PROJECT_PACKAGE}.platform.request_id")
request_id_from_header = request_id_module.request_id_from_header


def test_environment_parses_explicit_values(monkeypatch: pytest.MonkeyPatch) -> None:
    environment = Environment()
    monkeypatch.setenv("TEMPLATE_TEXT", " value ")
    monkeypatch.setenv("TEMPLATE_NUMBER", "42")
    monkeypatch.setenv("TEMPLATE_TRUE", "yes")
    monkeypatch.setenv("TEMPLATE_FALSE", "off")
    monkeypatch.setenv("TEMPLATE_LIST", " one, ,two ")

    assert environment.string("TEMPLATE_TEXT") == " value "
    assert environment.integer("TEMPLATE_NUMBER") == 42
    assert environment.boolean("TEMPLATE_TRUE") is True
    assert environment.boolean("TEMPLATE_FALSE") is False
    assert environment.list("TEMPLATE_LIST") == ["one", "two"]
    assert environment.string("MISSING_TEXT", "fallback") == "fallback"

    monkeypatch.setenv("TEMPLATE_NUMBER", "not-a-number")
    with pytest.raises(ImproperlyConfigured):
        environment.integer("TEMPLATE_NUMBER")
    monkeypatch.setenv("TEMPLATE_TRUE", "perhaps")
    with pytest.raises(ImproperlyConfigured):
        environment.boolean("TEMPLATE_TRUE")
    with pytest.raises(ImproperlyConfigured):
        environment.string("MISSING_REQUIRED")


@pytest.mark.django_db
def test_email_user_model_normalizes_identity_and_superuser_requirements() -> None:
    user = User.objects.create_user("Person@Example.Test", "Correct-horse-battery-1")

    assert user.email == "person@example.test"
    assert User.objects.get(email="person@example.test") == user
    assert User.objects.create_superuser(
        "admin@example.test", "Correct-horse-battery-1"
    ).is_staff

    with pytest.raises(ValueError, match="is_staff"):
        User.objects.create_superuser(
            "invalid@example.test", "Correct-horse-battery-1", is_staff=False
        )
    with pytest.raises(ValueError, match="required"):
        User.objects.create_user("", "Correct-horse-battery-1")


def test_platform_defaults_are_registered_and_safe(rf: RequestFactory) -> None:
    assert PlatformConfig.name.endswith(".platform")
    assert site._registry[User].__class__ is UserAdmin
    assert site._registry[AdminImpersonationAuditEvent].__class__.__name__ == (
        "AdminImpersonationAuditEventAdmin"
    )
    assert PrivateMediaStorage.location == "media"
    assert PrivateMediaStorage.default_acl == "private"
    assert PrivateMediaStorage.querystring_auth is True
    assert PublicStaticStorage.location == "static"
    assert PublicStaticStorage.default_acl is None
    assert PublicStaticStorage.querystring_auth is False
    if DomainTask is not None:
        assert DomainTask.autoretry_for == (ConnectionError, TimeoutError)
        assert DomainTask.retry_backoff is True
        assert DomainTask.retry_backoff_max == 300
        assert DomainTask.retry_jitter is True
        assert DomainTask.max_retries == 3
    assert account_settings(rf.get("/")) == {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION
    }
    assert settings.ENABLE_ADMIN_HIJACK is False
    assert settings.HIJACK_PERMISSION_CHECK.endswith(".platform.hijack.can_hijack")


def test_redaction_is_recursive_and_does_not_mutate_safe_values() -> None:
    payload = {
        "email": "person@example.test",
        "Authorization": "Bearer secret",
        "nested": {"password": "secret", "items": [{"token": "value"}]},
        "tuple": ({"cookie": "session"},),
    }

    redacted = redact_sensitive_data(None, "info", payload)

    assert redacted["email"] == "person@example.test"
    assert redacted["Authorization"] == REDACTED
    assert redacted["nested"]["password"] == REDACTED
    assert redacted["nested"]["items"][0]["token"] == REDACTED
    assert redacted["tuple"][0]["cookie"] == REDACTED


@pytest.mark.django_db
def test_health_and_error_endpoints_cover_success_and_failure(
    client: Client, monkeypatch: pytest.MonkeyPatch, rf: RequestFactory
) -> None:
    assert client.get("/livez/").json() == {"status": "ok"}
    assert client.get("/readyz/").json() == {"status": "ok"}

    health = import_module(f"{PROJECT_PACKAGE}.platform.health")

    monkeypatch.setattr(health.cache, "set", Mock(side_effect=RuntimeError("offline")))
    assert client.get("/readyz/").status_code == 503
    request = rf.get("/")
    assert handler403(request).status_code == 403
    assert handler403(request, Ratelimited()).status_code == 429
    assert handler404(request, Exception()).status_code == 404
    assert handler500(request).status_code == 500


@pytest.mark.django_db
def test_scaffold_commands_create_expected_files_and_reject_invalid_names(
    tmp_path: Path,
) -> None:
    output = StringIO()
    with override_settings(BASE_DIR=tmp_path):
        call_command("new_domain", "billing", stdout=output)
        project_package = settings.ROOT_URLCONF.partition(".")[0]
        domain = tmp_path / project_package / "domains" / "billing"
        assert (domain / "operations.py").exists()
        assert (domain / "tests" / "test_operations.py").exists()
        {% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
        assert (domain / "api.py").exists()
        {% endif -%}
        {% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
        assert (tmp_path / "hyper" / "routes" / "billing" / "entry.head.ts").exists()
        call_command("new_route", "settings/profile", stdout=output)
        assert (
            tmp_path / "hyper" / "routes" / "settings" / "profile" / "+page.py"
        ).exists()
        {% endif -%}
        with pytest.raises(CommandError):
            call_command("new_domain", "Billing")
        with override_settings(RENDERING_MODE="ssr"):
            call_command("new_domain", "server_only", stdout=output)
            assert not (domain.parent / "server_only" / "api.py").exists()
        with override_settings(RENDERING_MODE="api"):
            call_command("new_domain", "api_only", stdout=output)
            assert not (tmp_path / "hyper" / "routes" / "api_only").exists()
        with pytest.raises(CommandError):
            call_command("new_domain", "billing")
        {% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
        with pytest.raises(CommandError):
            call_command("new_route", "bad//route")
        with pytest.raises(CommandError):
            call_command("new_route", "settings/profile")
    {% endif -%}

    assert "Created domain 'billing'." in output.getvalue()


def test_request_identity_and_version_endpoint(client: Client) -> None:
    supplied = "release-2026.08.05"
    response = client.get("/livez/", headers={"X-Request-ID": supplied})
    generated = client.get("/livez/", headers={"X-Request-ID": "invalid"})
    version = client.get("/version/")

    assert response["X-Request-ID"] == supplied
    assert generated["X-Request-ID"] != "invalid"
    assert request_id_from_header("invalid") != "invalid"
    assert version.json() == {
        "version": settings.APP_VERSION,
        "build_sha": settings.APP_BUILD_SHA,
        "template_version": settings.TEMPLATE_VERSION,
        "rendering_mode": settings.RENDERING_MODE,
    }


@pytest.mark.django_db
def test_doctor_reports_dependencies_and_surfaces_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    doctor_module = import_module(
        f"{PROJECT_PACKAGE}.platform.management.commands.doctor"
    )
    DoctorCommand = doctor_module.Command

    output = StringIO()
    call_command("doctor", stdout=output)
    assert "PostgreSQL: ok" in output.getvalue()
    assert "Redis: ok" in output.getvalue()
    assert "Application diagnostics: ok" in output.getvalue()

    def unavailable_database() -> None:
        raise RuntimeError("offline")

    monkeypatch.setattr(
        DoctorCommand, "_check_database", staticmethod(unavailable_database)
    )
    with pytest.raises(CommandError, match="PostgreSQL: offline"):
        call_command("doctor")
