"""PostgreSQL-backed test settings; no SQLite compatibility escape hatch."""

from .base import *  # noqa: F403


DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "{{ cookiecutter.project_slug }}-tests",
    }
}
