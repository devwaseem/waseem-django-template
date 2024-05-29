"""
This file contains a definition for Content-Security-Policy headers.

Read more about it:
https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Content-Security-Policy

We are using `django-csp` to provide these headers.
Docs: https://github.com/mozilla/django-csp
"""
from {{cookiecutter.project_name}}.settings.components.storages import STORAGES

CSP_STATIC_URL = STORAGES["staticfiles"]["OPTIONS"]["base_url"]  # type: ignore
CSP_MEDIA_URL = STORAGES["default"]["OPTIONS"]["base_url"]  # type: ignore


if not CSP_STATIC_URL.startswith("http"):
    CSP_STATIC_URL = "http://localhost" + CSP_STATIC_URL

if not CSP_MEDIA_URL.startswith("http"):
    CSP_MEDIA_URL = "http://localhost" + CSP_MEDIA_URL

CSP_INCLUDE_NONCE_IN = ("script-src", "connect-src")
CSP_EXCLUDE_URL_PREFIXES = ("/admin",)
CSP_SCRIPT_SRC: tuple[str, ...] = (
    "'self'",
    "'unsafe-eval'",
    "https://unpkg.com",
    CSP_STATIC_URL,
)
CSP_IMG_SRC: tuple[str, ...] = (
    "'self'",
    "data:",  # Required by tailwind
    "http:",
    "https:",
    CSP_STATIC_URL,
    CSP_MEDIA_URL,
)
CSP_FONT_SRC: tuple[str, ...] = (
    "'self'",
    "https://fonts.googleapis.com",  # Google Fonts
    "https://fonts.gstatic.com",
    "data:",
    "'unsafe-inline'",
    CSP_STATIC_URL,
)
CSP_STYLE_SRC: tuple[str, ...] = (
    "'self'",
    "https://fonts.googleapis.com",
    "https://unpkg.com",
    "'unsafe-inline'",
    CSP_STATIC_URL,
)
CSP_MEDIA_SRC: tuple[str, ...] = (
    "'self'",
    "data:",
    CSP_STATIC_URL,
    CSP_MEDIA_URL,
)
CSP_DEFAULT_SRC: tuple[str, ...] = ("'self'",)
CSP_CONNECT_SRC: tuple[str, ...] = (
    "'self'",
    CSP_STATIC_URL,
    CSP_MEDIA_URL,
)
