from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.main"

    def ready(self) -> None:
        import server.apps.main.schema  # noqa: F401

        return super().ready()
