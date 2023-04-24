import os

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "team@server.app")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "team@server.app")


# Email
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)

