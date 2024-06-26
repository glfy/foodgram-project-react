from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("name", "color")
    save_on_top = True

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related("recipes__author")
        )
        return queryset


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    save_on_top = True

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related("recipes__author")
        )
        return queryset


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
    list_filter = ("author__username", "tags__name")
    list_display_links = ("name", "author")
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    inlines = [IngredientInRecipeInline]
    save_on_top = True

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_related("author")
            .prefetch_related("tags", "ingredients")
        )
        return queryset

    def favorited_by_users_count(self, object):
        return object.favorite.count()

    favorited_by_users_count.short_description = (
        "Количество добавлений в избранное"
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    list_display_links = ("recipe", "user")

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_related("recipe__author", "user")
        )
        return queryset


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    list_display_links = ("recipe", "user")

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_related("recipe__author", "user")
        )
        return queryset
