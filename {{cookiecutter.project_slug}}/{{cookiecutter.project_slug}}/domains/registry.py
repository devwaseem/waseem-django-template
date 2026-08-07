# fmt: off
"""Stable, project-owned extension points for template-managed code."""

from __future__ import annotations

from collections.abc import Sequence

from django.urls import URLPattern, URLResolver


INSTALLED_DOMAIN_APPS: tuple[str, ...] = ()


def extra_urlpatterns() -> Sequence[URLPattern | URLResolver]:
    """Return project-owned URL patterns registered by domain code."""
    return ()


{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
def register_api(_api: object) -> None:
    """Register project-owned API routers on the template-managed API."""
    return None
{% endif -%}
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
def dashboard_navigation() -> Sequence[dict[str, str]]:
    """Return project-owned navigation items for the authenticated shell."""
    return ()
{% endif -%}
