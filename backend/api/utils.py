from io import BytesIO

from django.db.models import Sum

from recipes.models import IngredientInRecipe


def create_shopping_list_file(ingredients):
    shopping_list = "\n".join(
        [
            f"{ing['ingredient__name']} - {ing['amount']} "
            f"{ing['ingredient__measurement_unit']}"
            for ing in ingredients
        ]
    )

    buffer = BytesIO()
    buffer.write(shopping_list.encode())
    buffer.seek(0)
    return buffer


def generate_shopping_list(user):
    ingredients = (
        IngredientInRecipe.objects.select_related()
        .filter(recipe__shopping_cart__user=user)
        .order_by("ingredient__name")
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(amount=Sum("amount"))
    )

    return create_shopping_list_file(ingredients)
