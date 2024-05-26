from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{cookiecutter.project_name}}"

    def ready(self) -> None:
        import {{cookiecutter.project_name}}.schema  # noqa: F401

        return super().ready()
