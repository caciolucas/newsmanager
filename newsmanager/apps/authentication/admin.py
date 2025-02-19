from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_admin", "groups", "user_permissions")},
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_admin",
    )
    filter_vertical = ("groups", "user_permissions")
