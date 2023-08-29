from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Subscription, User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_display_links = ("id", "email", "username", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.site_header = "Foodgram Admin"
admin.site.site_title = "Foodgram Admin"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "subscribed_to")
    search_fields = ("subscriber", "subscribed_to")
    list_display_links = ("subscriber", "subscribed_to")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("subscriber", "subscribed_to")
        )
