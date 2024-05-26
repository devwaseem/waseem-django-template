from env import Env
from {{cookiecutter.project_name}}.settings.vars import DEBUG

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/


ALLOWED_HOSTS = ["." + Env.str("DOMAIN_NAME")]

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
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ["https://*." + Env("DOMAIN_NAME")]

# csrf
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"


# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "same-origin"

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: dict[str, str | list[str]] = {}

# Only in production
if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

    # HSTS
    SECURE_HSTS_SECONDS = 63072000  # 2 years
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
