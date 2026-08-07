"""ASGI application initialized for direct Uvicorn serving."""

from __future__ import annotations

import os

from django.core.asgi import get_asgi_application

from {{ cookiecutter.project_slug }}.platform.telemetry import initialize_telemetry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_slug }}.settings.dev")
initialize_telemetry()
application = get_asgi_application()
