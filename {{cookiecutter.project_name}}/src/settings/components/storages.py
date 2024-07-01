from env import Env

from src.settings.components.aws import AWS_S3_CUSTOM_DOMAIN
from src.settings.vars import DEBUG

DJANGO_STATIC_HOST = Env.str("DJANGO_STATIC_HOST")
DJANGO_MEDIA_HOST = Env.str("DJANGO_MEDIA_HOST")

MEDIA_LOCATION = "media"
STATIC_LOCATION = "static" if DEBUG else "/var/www/static"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_LOCATION,
            "base_url": f"{DJANGO_MEDIA_HOST}/media/",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",  # noqa
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": f"{DJANGO_STATIC_HOST}/static/",
        },
    },
}


if Env.bool("MEDIA_USE_S3"):
    STORAGES["default"] = {
        "BACKEND": "src.settings.components.aws.PublicMediaStorage",
        "OPTIONS": {
            "location": MEDIA_LOCATION,
            "base_url": f"https://{AWS_S3_CUSTOM_DOMAIN}/media/",
        },
    }

if Env.bool("STATIC_USE_S3"):
    STORAGES["staticfiles"] = {
        "BACKEND": "src.settings.components.aws.StaticStorage",
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": f"https://{AWS_S3_CUSTOM_DOMAIN}/static/",
        },
    }

if Env.bool("STATIC_USE_WHITENOISE"):
    STORAGES["staticfiles"] = {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": f"{DJANGO_STATIC_HOST}/static/",
        },
    }
