from __future__ import annotations

from env import Env

from .base import *  # noqa: F403

DEBUG = False

USE_X_FORWARDED_HOST = Env.bool("USE_X_FORWARDED_HOST")
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https" if USE_SSL else "http",  # type: ignore[name-defined]  # noqa: F405
)

SECURE_HSTS_SECONDS = 63072000  # 2 years
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_RESOURCE_POLICY = "same-site"
