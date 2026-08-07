from importlib import import_module

from django.apps import AppConfig


class PlatformConfig(AppConfig):
    """Register the template-managed Django platform app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.project_slug }}.platform"
    label = "platform"

    def ready(self) -> None:
        """Connect platform signal handlers after Django initializes its app registry."""
        import_module(f"{self.name}.hijack")
