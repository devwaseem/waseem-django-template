"""Generic identity model; domain authorization uses Django permissions."""

from __future__ import annotations

from typing import ClassVar
from uuid import uuid7

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class UserManager(BaseUserManager["User"]):
    """Create email-only users and superusers."""

    use_in_migrations = True

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: object
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: object
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

    def _create_user(
        self, email: str, password: str | None, **extra_fields: object
    ) -> User:
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(
            email=self.normalize_email(email).strip().lower(), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """UUID, email-only user model with Django Groups and Permissions."""

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []
    objects = UserManager()

    def save(self, *args: object, **kwargs: object) -> None:
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("email",)
        constraints = [
            models.UniqueConstraint(
                Lower("email"), name="platform_user_email_ci_unique"
            ),
        ]


class AdminImpersonationAuditEvent(models.Model):
    """Append-only audit record for a privileged admin impersonation session."""

    class Action(models.TextChoices):
        """The only lifecycle transitions recorded for an impersonation session."""

        STARTED = "started", "Started"
        ENDED = "ended", "Ended"

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    action = models.CharField(max_length=16, choices=Action.choices)
    actor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="impersonation_audit_events_as_actor",
    )
    target = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="impersonation_audit_events_as_target",
    )
    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    request_id = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ("-occurred_at",)
        indexes = [
            models.Index(fields=("actor", "occurred_at")),
            models.Index(fields=("target", "occurred_at")),
        ]

    def __str__(self) -> str:
        """Provide a safe, useful identifier in the audit administration screen."""
        return f"{self.action}: {self.actor.email} -> {self.target.email}"
