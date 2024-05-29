# https://pypi.org/project/pyinstrument/3.0.0b3/#profile-a-web-request-in-django

from {{cookiecutter.project_name}}.settings.components.common import MIDDLEWARE

MIDDLEWARE += ["pyinstrument.middleware.ProfilerMiddleware"]
