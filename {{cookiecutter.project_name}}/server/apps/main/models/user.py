import os
import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager[AbstractUser]):
    """Manager class for User."""

    use_in_migrations = True

    def create_candidate(self, email: str, password: str):
        return self.create_user(
            email=email, password=password, role=User.Role.CANDIDATE
        )

    def create_user(
        self,
        email: str,
        password: str,
        role: "User.Role",
        **extra_fields,
    ) -> "User":
        """Create a Normal User."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, role=role, **extra_fields)

    def create_superuser(
        self,
        email=None,
        password=None,
        **extra_fields,
    ) -> "User":
        """Create a SuperUser with all the privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, role=User.Role.ADMIN, **extra_fields)

    def _create_user(
        self, email, password, role: "User.Role", **extra_fields
    ) -> "User":
        """Create and save a user with the given username, email, and password."""  # noqa: E501
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.role = role
        user.save(using=self._db)
        return user


def _avatar_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return f"images/{instance.id}/avatar{extension}"


class User(AbstractUser):
    """User class."""

    class Role(models.TextChoices):
        CANDIDATE = ("candidate", "Candidate")
        RECRUITER = ("recruiter", "Recruiter")
        ADMIN = ("admin", "Admin")

    internal_id = models.AutoField(primary_key=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = None  # type:ignore
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(_("Role"), choices=Role.choices, max_length=255)
    avatar = models.ImageField(
        "Avatar", upload_to=_avatar_upload_path, null=True, blank=True
    )
    signup_step = models.PositiveSmallIntegerField("Signup steps completed", default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()  # type:ignore
