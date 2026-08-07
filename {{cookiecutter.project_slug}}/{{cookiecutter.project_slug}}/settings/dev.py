"""Local-development settings with narrowly scoped convenience defaults."""

from .base import *  # noqa: F403


DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CONTENT_SECURITY_POLICY["DIRECTIVES"]["script-src"].append("http://localhost:5173")  # noqa: F405
CONTENT_SECURITY_POLICY["DIRECTIVES"]["style-src"].append("http://localhost:5173")  # noqa: F405
