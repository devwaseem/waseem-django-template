from typing import Iterable
from uuid import uuid4

from django.db import models

from src.models.base import TimeStampedModel


class APIKey(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)

    def save(
        self,
        force_insert: bool = False,  # noqa
        force_update: bool = False,  # noqa
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.key = "sk-" + str(uuid4())
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self) -> str:
        return self.name
