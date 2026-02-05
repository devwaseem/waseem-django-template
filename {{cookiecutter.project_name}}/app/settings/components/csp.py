"""
Content Security Policy (CSP) settings using Django's built-in support.
Docs: https://docs.djangoproject.com/en/6.0/howto/csp/
"""

from django.utils.csp import CSP

from app.settings.components.storages import MEDIA_URL, STATIC_URL
from app.settings.components.vite import (
    VITE_DEV_SERVER_HOST,
    VITE_DEV_SERVER_PORT,
    VITE_DEV_SERVER_URL,
)
from app.settings.flags import DEBUG

SECURE_CSP: dict[str, list[str]] = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [CSP.SELF, CSP.NONCE, "https://fonts.googleapis.com"],
    "font-src": [CSP.SELF, "https://fonts.gstatic.com", "data:"],
    "img-src": [CSP.SELF, "data:", "https:"],
    "connect-src": [CSP.SELF],
    "media-src": [CSP.SELF, "data:"],
}

if STATIC_URL.startswith("http"):
    for directive in (
        "script-src",
        "style-src",
        "font-src",
        "img-src",
        "connect-src",
        "media-src",
    ):
        SECURE_CSP[directive].append(STATIC_URL)

if MEDIA_URL.startswith("http"):
    for directive in ("img-src", "media-src", "connect-src"):
        SECURE_CSP[directive].append(MEDIA_URL)

if DEBUG:
    vite_ws = f"ws://{VITE_DEV_SERVER_HOST}:{VITE_DEV_SERVER_PORT}"
    SECURE_CSP["script-src"].append(VITE_DEV_SERVER_URL)
    SECURE_CSP["connect-src"].extend([VITE_DEV_SERVER_URL, vite_ws])
