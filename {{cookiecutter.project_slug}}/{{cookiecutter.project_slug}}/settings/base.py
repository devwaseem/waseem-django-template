# fmt: off
"""Secure, portable defaults shared by every runtime environment."""

from __future__ import annotations

{% if cookiecutter.rendering_mode in ["api", "hybrid"] %}
from datetime import timedelta
{% endif %}
from pathlib import Path
from typing import Any

import django_stubs_ext
import structlog
from csp.constants import NONE, NONCE, SELF
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

from {{ cookiecutter.project_slug }}.config.env import env
from {{ cookiecutter.project_slug }}.domains.registry import INSTALLED_DOMAIN_APPS
from {{ cookiecutter.project_slug }}.platform.logging import configure_logging


django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parents[2]
DEBUG = env.boolean("DEBUG", False)
SECRET_KEY = env.string("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
TIME_ZONE = "{{ cookiecutter.presentation_timezone }}"
USE_TZ = True
LANGUAGE_CODE = "en"
RENDERING_MODE = "{{ cookiecutter.rendering_mode }}"
APP_VERSION = env.string("APP_VERSION", "0.1.0")
APP_BUILD_SHA = env.string("APP_BUILD_SHA", "development")
TEMPLATE_VERSION = "1.0.0"
USE_I18N = False

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"
ASGI_APPLICATION = "{{ cookiecutter.project_slug }}.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "csp",
    "storages",
    "django_structlog",
    "django_ratelimit",
    "allauth",
    "allauth.account",
    "{{ cookiecutter.project_slug }}.platform.apps.PlatformConfig",
    *INSTALLED_DOMAIN_APPS,
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
    "hyperdjango",
    "django_cotton",
{% endif -%}
{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
    "ninja_extra",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
{% endif -%}
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "{{ cookiecutter.project_slug }}.platform.request_id.RequestIDMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_ratelimit.middleware.RatelimitMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "{{ cookiecutter.project_slug }}" / "platform" / "templates",
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
            BASE_DIR / "hyper",
{% endif -%}
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "{{ cookiecutter.project_slug }}.platform.context_processors.account_settings",
            ],
        },
    }
]

AUTH_USER_MODEL = "platform.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
SITE_ID = env.integer("SITE_ID", 1)
LOGIN_URL = reverse_lazy("account_login")
LOGIN_REDIRECT_URL = "/"
ACCOUNT_ALLOW_REGISTRATION = env.boolean("ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USER_MODEL_USERNAME_FIELD: str | None = None

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.string("POSTGRES_DB"),
        "USER": env.string("POSTGRES_USER"),
        "PASSWORD": env.string("POSTGRES_PASSWORD"),
        "HOST": env.string("POSTGRES_HOST"),
        "PORT": env.integer("POSTGRES_PORT", 5432),
        "CONN_MAX_AGE": env.integer("CONN_MAX_AGE", 60),
        "OPTIONS": {"connect_timeout": env.integer("DB_CONNECT_TIMEOUT", 10)},
    }
}

REDIS_URL = env.string("REDIS_URL")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_USE_S3 = env.boolean("STATIC_USE_S3", False)
MEDIA_USE_S3 = env.boolean("MEDIA_USE_S3", False)
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] -%}
HYPER_FRONTEND_DIR = BASE_DIR / "hyper"
HYPER_VITE_OUTPUT_DIR = BASE_DIR / "dist"
HYPER_VITE_DEV_SERVER_URL = "http://localhost:5173/"
HYPER_DEV = DEBUG
STATICFILES_DIRS = [HYPER_VITE_OUTPUT_DIR] if HYPER_VITE_OUTPUT_DIR.exists() else []
{% endif -%}

if STATIC_USE_S3 or MEDIA_USE_S3:
    AWS_ACCESS_KEY_ID = env.string("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.string("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.string("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env.string("AWS_S3_REGION_NAME")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    STORAGES: dict[str, dict[str, Any]] = {
        "default": {
            "BACKEND": (
                "{{ cookiecutter.project_slug }}.platform.storage.PrivateMediaStorage"
                if MEDIA_USE_S3
                else "django.core.files.storage.FileSystemStorage"
            ),
        },
        "staticfiles": {
            "BACKEND": (
                "{{ cookiecutter.project_slug }}.platform.storage.PublicStaticStorage"
                if STATIC_USE_S3
                else "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    }

EMAIL_BACKEND = env.string(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env.string("EMAIL_HOST", "localhost")
EMAIL_PORT = env.integer("EMAIL_PORT", 1025)
EMAIL_HOST_USER = env.string("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.string("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.boolean("EMAIL_USE_TLS", False)
DEFAULT_FROM_EMAIL = env.string("DEFAULT_FROM_EMAIL", "no-reply@example.com")
SERVER_EMAIL = env.string("SERVER_EMAIL", "system@example.com")

USE_SSL = env.boolean("USE_SSL", False)
SESSION_COOKIE_SECURE = USE_SSL
CSRF_COOKIE_SECURE = USE_SSL
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = False
SECURE_SSL_REDIRECT = USE_SSL
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "base-uri": [NONE],
        "default-src": [SELF],
        "form-action": [SELF],
        "frame-ancestors": [NONE],
        "img-src": [SELF, "data:"],
        "object-src": [NONE],
        "script-src": [SELF, NONCE],
        "style-src": [SELF],
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: "info",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

configure_logging(debug=DEBUG)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
{% if cookiecutter.rendering_mode in ["api", "hybrid"] -%}
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
{% endif -%}
