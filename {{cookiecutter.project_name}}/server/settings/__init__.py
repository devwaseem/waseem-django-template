"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from pathlib import Path
from typing import Literal

import django_stubs_ext
from django.core.exceptions import ImproperlyConfigured
from split_settings.tools import include

from env import Env

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV: Literal["development", "production", "test"] = (
    Env("DJANGO_ENV") or "development"
)

if ENV not in ["development", "production", "test"]:
    raise ImproperlyConfigured(
        "DJANGO_ENV can only be one of [development|production|test]"
    )


base_settings = [
    "components/common.py",
    "components/allauth.py",
    "components/database.py",
    "components/caches.py",
    "components/emails.py",
    "components/logging.py",
    "components/csp.py",
    # You can even use glob:
    # 'components/*.py'
    # Select the right env:
    f"environments/{ENV}.py",
]


# Include settings:
include(*base_settings)
