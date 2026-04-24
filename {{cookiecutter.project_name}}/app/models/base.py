import uuid
from datetime import datetime
from uuid import UUID

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField[datetime, datetime](auto_now_add=True)
    modified_at = models.DateTimeField[datetime, datetime](auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField[UUID, UUID](
        default=uuid.uuid7,
        primary_key=True,
        editable=False,
    )

    class Meta:
        abstract = True


class TimestampedUUIDModel(TimeStampedModel, UUIDModel):
    class Meta(TimeStampedModel.Meta, UUIDModel.Meta):
        abstract = True
