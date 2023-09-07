from env import Env

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = Env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = Env("SERVER_EMAIL")


EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = Env(
    "EMAIL_BACKEND", str, "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = Env("EMAIL_HOST")
EMAIL_HOST_USER = Env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = Env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = Env("EMAIL_PORT")
