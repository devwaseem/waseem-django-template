from {{cookiecutter.project_name}}.settings.components.common import MIDDLEWARE


MIDDLEWARE += [
    "pyinstrument.middleware.ProfilerMiddleware"
]

def custom_show_pyinstrument(request):
    return request.user.is_superuser


PYINSTRUMENT_SHOW_CALLBACK = f"{__name__}.custom_show_pyinstrument"
