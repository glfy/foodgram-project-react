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
        if not self.request.user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(favorited_by_users=self.request.user.id)
        return queryset.filter(~Q(favorited_by_users=self.request.user.id))

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(
                recipes_in_shopping_cart=self.request.user.id
            )
        return queryset.filter(
            ~Q(recipes_in_shopping_cart=self.request.user.id)
        )
