from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src"

    def ready(self) -> None:
        import src.schema  # noqa: F401

        return super().ready()
