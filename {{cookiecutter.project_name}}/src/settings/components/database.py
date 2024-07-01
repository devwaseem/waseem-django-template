from env import Env

from src.settings.vars import TEST

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": Env("POSTGRES_DB"),
        "USER": Env("POSTGRES_USER"),
        "PASSWORD": Env("POSTGRES_PASSWORD"),
        "HOST": Env("DJANGO_DATABASE_HOST"),
        "PORT": Env("DJANGO_DATABASE_PORT"),
        "CONN_MAX_AGE": Env("CONN_MAX_AGE"),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}

if TEST:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
