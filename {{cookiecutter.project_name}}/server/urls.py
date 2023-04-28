"""
URL Configuration for {{cookiecutter.project_verbose_name}}

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static  # noqa: WPS433
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path
from django.views.generic import TemplateView

from server.apps.main import urls as main_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("allauth.urls")), #django allauth urls
    path("", include(main_urls)),
    # Text and xml static files:
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="txt/robots.txt",
            content_type="text/plain",
        ),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="txt/humans.txt",
            content_type="text/plain",
        ),
    ),
] + static(  # noqa
    settings.STATIC_URL,  # type: ignore
    document_root=settings.STATIC_ROOT,
)


def handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "errors/404.html", {"exception": exception})


def handler403(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "errors/403.html", {"exception": exception})


def handler500(request: HttpRequest) -> HttpResponse:
    return render(request, "errors/500.html", {})


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433

    urlpatterns = [
        # Django silk
        # path("silk/", include("silk.urls", namespace="silk")),
        path("__reload__/", include("django_browser_reload.urls")),
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
