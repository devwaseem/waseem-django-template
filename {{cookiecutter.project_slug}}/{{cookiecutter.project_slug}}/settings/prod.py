"""Production settings that fail closed for missing security configuration."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


DEBUG = False
SECURE_HSTS_SECONDS = env.integer("SECURE_HSTS_SECONDS", 31536000)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured("ALLOWED_HOSTS must be set in production.")
if SECRET_KEY in {"", "replace-me"}:  # noqa: F405
    raise ImproperlyConfigured("SECRET_KEY must be set to a secure value.")
if not USE_SSL:  # noqa: F405
    raise ImproperlyConfigured("USE_SSL must be true in production.")
if "*" in CORS_ALLOWED_ORIGINS:  # noqa: F405
    raise ImproperlyConfigured(
        "CORS_ALLOWED_ORIGINS must not contain a wildcard in production."
    )
if METRICS_ENABLED and not METRICS_TOKEN:  # noqa: F405
    raise ImproperlyConfigured(
        "METRICS_TOKEN must be set when METRICS_ENABLED is true in production."
    )
