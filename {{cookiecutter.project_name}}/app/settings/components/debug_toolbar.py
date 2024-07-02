# https://django-debug-toolbar.readthedocs.io

from typing import cast

from django.http import HttpRequest

from app.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from app.settings.vars import DEBUG

INSTALLED_APPS += [
    "debug_toolbar",
    "debug_toolbar_line_profiler",
    "template_profiler_panel",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "debug_toolbar_line_profiler.panel.ProfilingPanel",
    "template_profiler_panel.panels.template.TemplateProfilerPanel",
]


def django_debug_toolbar_show_only_for_admins(request: HttpRequest) -> bool:
    if user := request.user:
        return cast(bool, user.is_authenticated and user.is_superuser)  # type: ignore
    return False


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "debug_toolbar.middleware.show_toolbar"
    if DEBUG
    else "app.settings.debug_toolbar.django_debug_toolbar_show_only_for_admins"
}
