"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from pathlib import Path

import django_stubs_ext
from split_settings.tools import include

from env import Env

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = Env("DJANGO_ENV") or "development"


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
