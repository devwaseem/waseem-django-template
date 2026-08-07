{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
from __future__ import annotations

import pytest
from django.test import Client, RequestFactory

from {{ cookiecutter.project_slug }}.platform.models import User
from hyper.layouts.dashboard.layout import DashboardLayout


@pytest.mark.django_db
def test_server_rendered_auth_and_dashboard_shell(
    client: Client, rf: RequestFactory
) -> None:
    assert client.get("/").status_code == 302
    assert client.get("/login/").status_code == 200
    assert client.get("/register/").status_code == 200
    user = User.objects.create_user("person@example.test", "Correct-horse-battery-1")
    client.force_login(user)
    home = client.get("/")
    assert home.status_code == 200
    assert b"Start with a product domain" in home.content

    request = rf.get("/")
    request.resolver_match = None
    request.user = user
    context = DashboardLayout(title="Dashboard").get_context(request)
    assert context["dashboard_site_name"] == "{{ cookiecutter.project_name }}"
    assert context["sidebar_items"][0]["active"] is False
{% endif -%}
