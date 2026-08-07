"""Generic authenticated shell with product navigation supplied by the registry."""

from __future__ import annotations

from typing import Any, TypedDict

from django.http import HttpRequest

from {{ cookiecutter.project_slug }}.domains.registry import dashboard_navigation
from hyper.layouts.base import BaseLayout


class DashboardSidebarItem(TypedDict):
    label: str
    href: str
    active: bool


class DashboardLayout(BaseLayout):
    """Add shared navigation and current-user context to authenticated pages."""

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        context = super().get_context(request=request)
        current_url_name = (
            request.resolver_match.url_name if request.resolver_match else ""
        )
        sidebar_items: list[DashboardSidebarItem] = [
            {"label": "Home", "href": "/", "active": current_url_name == "home"},
            *[
                {**item, "active": item.get("active", False)}
                for item in dashboard_navigation()
            ],
        ]
        context["sidebar_items"] = sidebar_items
        context["dashboard_site_name"] = "{{ cookiecutter.project_name }}"
        return context
