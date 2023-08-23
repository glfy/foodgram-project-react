from django_filters import FilterSet, filters

from django.db.models import Q

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.NumberFilter(method="filter_is_favorited")

    is_in_shopping_cart = filters.NumberFilter(
        method="filter_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(favorite__user=user)
        return queryset.filter(~Q(favorite__user=user))

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(shopping_cart__user=user)
        return queryset.filter(~Q(shopping__cart=user))
