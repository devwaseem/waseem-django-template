"""Validate Cookiecutter inputs before any project files are rendered."""

from __future__ import annotations

import re
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PRESENTATION_TIMEZONE = "{{ cookiecutter.presentation_timezone }}"
RENDERING_MODE = "{{ cookiecutter.rendering_mode }}"
ENABLE_CELERY = "{{ cookiecutter.enable_celery }}"
LICENSE = "{{ cookiecutter.license }}"


def fail(message: str) -> None:
    """Abort rendering with one actionable validation message."""
    print(f"Cookiecutter input error: {message}", file=sys.stderr)
    raise SystemExit(1)


if not re.fullmatch(r"[a-z][a-z0-9_]*", PROJECT_SLUG):
    fail(
        "project_slug must be a lowercase Python identifier starting with a "
        "letter; use letters, numbers, and underscores only."
    )

try:
    ZoneInfo(PRESENTATION_TIMEZONE)
except ZoneInfoNotFoundError:
    fail(
        "presentation_timezone must be a valid IANA time zone, for example "
        "America/Toronto."
    )

if RENDERING_MODE not in {"api", "ssr", "hybrid"}:
    fail("rendering_mode must be api, ssr, or hybrid.")

if ENABLE_CELERY not in {"yes", "no"}:
    fail("enable_celery must be yes or no.")

if LICENSE not in {"Proprietary", "MIT", "Apache-2.0"}:
    fail("license must be Proprietary, MIT, or Apache-2.0.")
