from __future__ import annotations

from typing import Any, TypedDict

from django.http import HttpRequest

from app.context_processors import get_site_data
from hyper.layouts.base import BaseLayout


class DashboardSidebarItem(TypedDict):
    label: str
    href: str
    icon: str
    active: bool


class DashboardLayout(BaseLayout):
    def __init__(self, title: str) -> None:
        super().__init__(title=title)
        self.sidebar_items: list[DashboardSidebarItem] = []

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        context = super().get_context(request=request)
        current_url_name = (
            request.resolver_match.url_name if request.resolver_match else None
        )
        site_data = get_site_data(request=request)
        site_name = site_data["site_name"] or "Your App"

        sidebar_items: list[DashboardSidebarItem] = [
            {
                "label": "Dashboard",
                "href": "/",
                "icon": "icon-[solar--widget-5-linear]",
                "active": current_url_name == "home",
            },
            {
                "label": "Inbox",
                "href": "#",
                "icon": "icon-[solar--inbox-linear]",
                "active": False,
            },
            {
                "label": "Reports",
                "href": "#",
                "icon": "icon-[solar--chart-square-linear]",
                "active": False,
            },
            {
                "label": "Settings",
                "href": "#",
                "icon": "icon-[solar--settings-linear]",
                "active": False,
            },
        ]

        self.sidebar_items = sidebar_items
        context["sidebar_items"] = sidebar_items
        context["dashboard_site_name"] = site_name
        return context
