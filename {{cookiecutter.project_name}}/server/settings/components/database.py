from server.settings import env

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("DJANGO_DATABASE_HOST"),
        "PORT": env("DJANGO_DATABASE_PORT", int,  5432),
        "CONN_MAX_AGE": env("CONN_MAX_AGE", int, 60),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}
