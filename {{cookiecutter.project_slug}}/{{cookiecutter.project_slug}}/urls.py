"""Top-level routes deliberately kept thin and explicit."""

from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from {{ cookiecutter.project_slug }}.domains.registry import extra_urlpatterns
from {{ cookiecutter.project_slug }}.platform.health import livez, readyz, version
from {{ cookiecutter.project_slug }}.platform.metrics import metrics


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hijack/", include("hijack.urls")),
    path("livez/", livez, name="livez"),
    path("readyz/", readyz, name="readyz"),
    path("version/", version, name="version"),
    path("metrics/", metrics, name="metrics"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="txt/robots.txt", content_type="text/plain"),
    ),
]

{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
if settings.DEBUG and getattr(settings, "HYPER_DEBUG_TOOLBAR", False):
    urlpatterns.append(
        path(
            "__hyperdebug__/",
            include("hyperdjango.integrations.devtools.urls"),
        )
    )
{% endif -%}

urlpatterns.extend(extra_urlpatterns())

{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
from {{ cookiecutter.project_slug }}.api.router import api

urlpatterns.append(path("api/v1/", api.urls))
{% endif -%}
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
from hyperdjango.urls import include_routes

urlpatterns.extend(include_routes())
{% endif -%}

if settings.DEBUG:  # pragma: no cover - development convenience only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

platform_views = f"{__package__}.platform.views"
handler403 = f"{platform_views}.handler403"
handler404 = f"{platform_views}.handler404"
handler500 = f"{platform_views}.handler500"
