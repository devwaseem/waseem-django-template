from typing import Any
from uuid import uuid4

from django.db import models

from app.models.base import TimeStampedModel


class APIKey(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)

    def save(  # type: ignore
        self,
        *args: Any,
        force_insert: bool = False,
        force_update: bool = False,
        using: Any | None = None,
        update_fields: Any | None = None,
    ) -> None:
        self.key = "sk-" + str(uuid4())
        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self) -> str:
        return self.name
