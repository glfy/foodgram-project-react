from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_subscribed",
    )
    list_filter = ("email", "username", "first_name")
    search_fields = ("username", "email", "first_name", "last_name")


admin.site.site_header = (
    "Foodgram Admin"  # Optional: Set the admin site header
)
admin.site.site_title = "Foodgram Admin"  # Optional: Set the admin site title

# Register your User model using the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
