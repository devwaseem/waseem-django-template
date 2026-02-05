"""
WSGI config for the project

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{ cookiecutter.django_settings_module_default }}",
)

application = get_wsgi_application()
