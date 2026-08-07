"""Generic identity model; domain authorization uses Django permissions."""

from __future__ import annotations

from typing import ClassVar
from uuid import uuid7

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower


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
