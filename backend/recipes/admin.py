from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag
from django.shortcuts import get_object_or_404


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("name", "color")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author__username", "name", "tags__name")
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    inlines = [IngredientInRecipeInline]
    fieldsets = (
        (
            "Recipe Details",
            {
                "fields": (
                    "name",
                    "author",
                    "favorited_by_users_count",
                    "image",
                    "text",
                    "cooking_time",
                    "tags",
                ),
            },
        ),
    )
    readonly_fields = ("favorited_by_users_count",)

    def favorited_by_users_count(self, obj):
        return obj.favorited_by_users.count()

    favorited_by_users_count.short_description = "Добавлено в избранное"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        recipe = get_object_or_404(Recipe, pk=object_id)
        extra_context = extra_context or {}
        extra_context["favorited_by_users_count"] = self.favorited_by_users_count(
            recipe
        )
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )
