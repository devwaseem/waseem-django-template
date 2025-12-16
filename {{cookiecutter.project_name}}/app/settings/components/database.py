from app.settings.flags import TEST
from env import Env

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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
