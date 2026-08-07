"""Top-level routes deliberately kept thin and explicit."""

from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from {{ cookiecutter.project_slug }}.domains.registry import extra_urlpatterns
from {{ cookiecutter.project_slug }}.platform.health import livez, readyz, version


urlpatterns = [
    path("admin/", admin.site.urls),
    path("livez/", livez, name="livez"),
    path("readyz/", readyz, name="readyz"),
    path("version/", version, name="version"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="txt/robots.txt", content_type="text/plain"),
    ),
]

urlpatterns.extend(extra_urlpatterns())

{% if cookiecutter.rendering_mode in ["api", "hybrid"] %}
from {{ cookiecutter.project_slug }}.api.router import api

urlpatterns.append(path("api/v1/", api.urls))
{% endif %}
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
from hyperdjango.urls import include_routes

urlpatterns.extend(include_routes())
{% endif %}

if settings.DEBUG:  # pragma: no cover - development convenience only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "{{ cookiecutter.project_slug }}.platform.views.handler403"
handler404 = "{{ cookiecutter.project_slug }}.platform.views.handler404"
handler500 = "{{ cookiecutter.project_slug }}.platform.views.handler500"
