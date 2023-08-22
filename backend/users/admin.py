from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Subscription


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("email", "username", "first_name")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.site_header = "Foodgram Admin"
admin.site.site_title = "Foodgram Admin"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "subscribed_to")
    search_fields = ("subscriber", "subscribed_to")
