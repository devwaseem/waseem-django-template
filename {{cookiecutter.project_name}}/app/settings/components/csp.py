"""
This file contains a definition for Content-Security-Policy headers.

Read more about it:
https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Content-Security-Policy

We are using `django-csp` to provide these headers.
Docs: https://github.com/mozilla/django-csp
"""

from app.settings.components.storages import MEDIA_URL, STATIC_URL

CSP_INCLUDE_NONCE_IN = ("script-src", "connect-src")
CSP_EXCLUDE_URL_PREFIXES = ("/admin",)
CSP_SCRIPT_SRC: tuple[str, ...] = (
    "'self'",
    "'unsafe-eval'",
    "https://unpkg.com",
    STATIC_URL,
)
CSP_IMG_SRC: tuple[str, ...] = (
    "'self'",
    "data:",  # Required by tailwind
    "http:",
    "https:",
    STATIC_URL,
    MEDIA_URL,
)
CSP_FONT_SRC: tuple[str, ...] = (
    "'self'",
    "https://fonts.googleapis.com",  # Google Fonts
    "https://fonts.gstatic.com",
    "data:",
    "'unsafe-inline'",
    STATIC_URL,
)
CSP_STYLE_SRC: tuple[str, ...] = (
    "'self'",
    "https://fonts.googleapis.com",
    "https://unpkg.com",
    "'unsafe-inline'",
    STATIC_URL,
)
CSP_MEDIA_SRC: tuple[str, ...] = (
    "'self'",
    "data:",
    STATIC_URL,
    MEDIA_URL,
)
CSP_DEFAULT_SRC: tuple[str, ...] = ("'self'",)
CSP_CONNECT_SRC: tuple[str, ...] = (
    "'self'",
    STATIC_URL,
    MEDIA_URL,
)
