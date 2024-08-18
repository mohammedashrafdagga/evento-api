from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    # Fields to be displayed in the list view of the admin panel
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "dob",
        "sex",
        "country",
        "profile_image",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "sex", "country")

    # Fields to be displayed in the form when editing or creating a user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "dob",
                    "sex",
                    "country",
                    "profile_image",
                )
            },
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
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields to be displayed when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "dob",
                    "sex",
                    "country",
                    "profile_image",
                ),
            },
        ),
    )

    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)


# Register the customized UserAdmin
admin.site.register(User, UserAdmin)
