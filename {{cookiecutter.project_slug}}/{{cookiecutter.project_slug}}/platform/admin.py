"""Django Unfold admin registration for the generic user model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from hijack.contrib.admin import HijackUserAdminMixin

from .models import AdminImpersonationAuditEvent, User


@admin.register(User)
class UserAdmin(HijackUserAdminMixin, BaseUserAdmin[User]):
    """Admin management for the email-only user model."""

    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "password1", "password2", "is_staff", "is_superuser")},
        ),
    )


@admin.register(AdminImpersonationAuditEvent)
class AdminImpersonationAuditEventAdmin(admin.ModelAdmin[AdminImpersonationAuditEvent]):
    """Expose immutable impersonation events to superusers for review."""

    list_display = (
        "occurred_at",
        "action",
        "actor",
        "target",
        "ip_address",
        "request_id",
    )
    list_filter = ("action",)
    search_fields = ("actor__email", "target__email", "request_id")
    readonly_fields = (
        "id",
        "action",
        "actor",
        "target",
        "occurred_at",
        "ip_address",
        "request_id",
    )
    ordering = ("-occurred_at",)

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Keep impersonation audit visibility restricted to active superusers."""
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(
        self,
        request: HttpRequest,
        obj: AdminImpersonationAuditEvent | None = None,
    ) -> bool:
        """Allow audit review but not audit modification."""
        return request.user.is_active and request.user.is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Prevent manual creation of audit records."""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: AdminImpersonationAuditEvent | None = None,
    ) -> bool:
        """Prevent updates to historically recorded events."""
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: AdminImpersonationAuditEvent | None = None,
    ) -> bool:
        """Prevent deletion of historically recorded events."""
        return False
