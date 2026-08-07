"""Production configuration contracts for generated projects."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PROBE = """
import json
import django

django.setup()

from django.conf import settings
from {{ cookiecutter.project_slug }}.platform.logging import redact_sensitive_data
from {{ cookiecutter.project_slug }}.platform.storage import (
    PrivateMediaStorage,
    PublicStaticStorage,
)

redacted = redact_sensitive_data(
    None,
    "info",
    {"Authorization": "Bearer secret", "nested": {"password": "secret"}},
)
print(json.dumps({
    "csp": {
        directive: [str(source) for source in sources]
        for directive, sources in settings.CONTENT_SECURITY_POLICY["DIRECTIVES"].items()
    },
    "session_cookie_secure": settings.SESSION_COOKIE_SECURE,
    "csrf_cookie_secure": settings.CSRF_COOKIE_SECURE,
    "session_cookie_httponly": settings.SESSION_COOKIE_HTTPONLY,
    "csrf_cookie_httponly": settings.CSRF_COOKIE_HTTPONLY,
    "cors_allow_all": settings.CORS_ALLOW_ALL_ORIGINS,
    "cors_origins": settings.CORS_ALLOWED_ORIGINS,
    "media_backend": settings.STORAGES["default"]["BACKEND"],
    "static_backend": settings.STORAGES["staticfiles"]["BACKEND"],
    "media_private": (
        PrivateMediaStorage.default_acl == "private"
        and PrivateMediaStorage.querystring_auth is True
    ),
    "static_public": (
        PublicStaticStorage.default_acl is None
        and PublicStaticStorage.querystring_auth is False
    ),
    "redacted": redacted,
}))
"""


def production_environment(*, use_s3: bool = False) -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "DJANGO_SETTINGS_MODULE": "{{ cookiecutter.project_slug }}.settings.prod",
            "DEBUG": "false",
            "SECRET_KEY": "production-check-secret-key-that-is-long-and-not-used-anywhere",
            "ALLOWED_HOSTS": "production-check.example.test",
            "USE_SSL": "true",
            "POSTGRES_DB": "production_check",
            "POSTGRES_USER": "production_check",
            "POSTGRES_PASSWORD": "production_check",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "REDIS_URL": "redis://127.0.0.1:6379/0",
            "STATIC_USE_S3": str(use_s3).lower(),
            "MEDIA_USE_S3": str(use_s3).lower(),
            "AWS_ACCESS_KEY_ID": "production-check-access-key",
            "AWS_SECRET_ACCESS_KEY": "production-check-secret-key",
            "AWS_STORAGE_BUCKET_NAME": "production-check-bucket",
            "AWS_S3_REGION_NAME": "eu-west-1",
        }
    )
    return environment


def run_production_command(
    environment: dict[str, str], *arguments: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603, RUF100 - fixed local interpreter and arguments.
        [sys.executable, *arguments],
        cwd=PROJECT_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def check_production_settings(
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return run_production_command(environment, "manage.py", "check", "--deploy")


def inspect_production_settings(environment: dict[str, str]) -> dict[str, object]:
    result = run_production_command(environment, "-c", SETTINGS_PROBE)

    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_production_check_passes_with_complete_safe_configuration() -> None:
    result = check_production_settings(production_environment())

    assert result.returncode == 0, result.stderr


def test_production_security_contract_holds_for_cookies_csp_cors_and_logging() -> None:
    runtime = inspect_production_settings(production_environment())
    csp = runtime["csp"]
    all_sources = {source for sources in csp.values() for source in sources}

    assert runtime["session_cookie_secure"] is True
    assert runtime["csrf_cookie_secure"] is True
    assert runtime["session_cookie_httponly"] is True
    assert runtime["csrf_cookie_httponly"] is True
    assert runtime["cors_allow_all"] is False
    assert runtime["cors_origins"] == []
    assert "unsafe-inline" not in all_sources
    assert "unsafe-eval" not in all_sources
    assert runtime["redacted"] == {
        "Authorization": "[REDACTED]",
        "nested": {"password": "[REDACTED]"},
    }


def test_production_storage_contract_keeps_media_private_and_static_public() -> None:
    runtime = inspect_production_settings(production_environment(use_s3=True))

    assert runtime["media_backend"].endswith(".PrivateMediaStorage")
    assert runtime["static_backend"].endswith(".PublicStaticStorage")
    assert runtime["media_private"] is True
    assert runtime["static_public"] is True


def test_production_settings_fail_closed_without_allowed_hosts() -> None:
    environment = production_environment()
    environment.pop("ALLOWED_HOSTS")

    result = check_production_settings(environment)

    assert result.returncode != 0
    assert "ALLOWED_HOSTS must be set in production." in result.stderr


def test_production_settings_reject_wildcard_cors_origins() -> None:
    environment = production_environment()
    environment["CORS_ALLOWED_ORIGINS"] = "https://console.example.test,*"

    result = check_production_settings(environment)

    assert result.returncode != 0
    assert "CORS_ALLOWED_ORIGINS must not contain a wildcard" in result.stderr
