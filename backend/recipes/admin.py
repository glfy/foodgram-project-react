from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientInRecipe, Recipe, Tag, Favorite
from django.db.models import Count


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("name", "color")
    save_on_top = True


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    save_on_top = True


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "favorited_by_users_count",
    )
    list_filter = ("author__username", "name", "tags__name")
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    inlines = [IngredientInRecipeInline]
    save_on_top = True

    def favorited_by_users_count(self, object):
        """Вычисляет количество добавлений рецепта в избранное."""
        return object.favorite.count()

    favorited_by_users_count.short_description = (
        "Количество добавлений в избранное"
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
