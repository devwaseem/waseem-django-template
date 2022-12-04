import uuid

from django.db import models


class BaseUUIDModel(models.Model):
    internal_id = models.AutoField(primary_key=True, editable=False)
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
