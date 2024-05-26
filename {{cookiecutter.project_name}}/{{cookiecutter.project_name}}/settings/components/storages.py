from env import Env
from {{cookiecutter.project_name}}.settings.vars import DEBUG
from {{cookiecutter.project_name}}.settings.components.aws import AWS_S3_CUSTOM_DOMAIN

DJANGO_STATIC_HOST = Env.str("DJANGO_STATIC_HOST", "")
DJANGO_MEDIA_HOST = Env.str("DJANGO_MEDIA_HOST", "")

STATIC_LOCATION = "static" if DEBUG else "/var/www/static"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "media",
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


if Env.bool("MEDIA_USE_S3", False):
    STORAGES["default"] = {
        "BACKEND": "{{cookiecutter.project_name}}.settings.components.aws.PublicMediaStorage", # noqa
        "location": "media",
        "base_url": f"https://{AWS_S3_CUSTOM_DOMAIN}/media/",
    }

if Env.bool("STATIC_USE_S3", False):
    STORAGES["staticfiles"] = {
        "BACKEND": "{{cookiecutter.project_name}}.settings.components.aws.StaticStorage", # noqa
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": f"https://{AWS_S3_CUSTOM_DOMAIN}/static/",
        },
    }
elif Env.bool("STATIC_USE_WHITENOISE", False):
    STORAGES["staticfiles"] = {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_LOCATION,
            "base_url": f"{DJANGO_STATIC_HOST}/static/",
        },
    }
