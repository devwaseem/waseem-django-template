from env import Env

from app.settings.vars import DEBUG

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

USE_SSL = Env.bool("USE_SSL")

ALLOWED_HOSTS = Env.list("ALLOWED_HOSTS", [])


if DEBUG:
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# session
SESSION_COOKIE_SECURE = USE_SSL
SESSION_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = Env.list("CSRF_TRUSTED_ORIGINS", [])

# csrf
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = USE_SSL
CSRF_COOKIE_SAMESITE = "Strict"


SECURE_SSL_REDIRECT = USE_SSL

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "same-origin"

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: dict[str, str | list[str]] = {}

# Only in production
if not DEBUG:
    USE_X_FORWARDED_HOST = Env.bool("USE_X_FORWARDED_HOST")
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https" if USE_SSL else "http",
    )

    # HSTS
    SECURE_HSTS_SECONDS = 63072000  # 2 years
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
