from typing import ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager[AbstractUser]):
    """Manager class for User."""

    use_in_migrations = True

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: str | int | bool,
    ) -> "User":
        """Create a Normal User."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: str | int | bool,
    ) -> "User":
        """Create a SuperUser with all the privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(
        self,
        email: str,
        password: str,
        **extra_fields: str | int | bool,
    ) -> "User":
        """Create and save a user with the given username, email, and password."""  # noqa: E501
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """User class."""

    id = models.AutoField(primary_key=True)
    username = None  # type:ignore
    email = models.EmailField(_("email address"), unique=True)

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []
    objects = UserManager()  # type:ignore
