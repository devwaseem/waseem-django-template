from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from app.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin[User]):
    ordering = ["email"]
    list_display = (
        "email",
        "name",
        "phone_number",
        "is_staff",
        "is_insolvency_professional",
    )
    search_fields = ("name", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("name", "phone_number", "is_insolvency_professional")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "phone_number",
                    "is_insolvency_professional",
                ),
            },
        ),
    )
