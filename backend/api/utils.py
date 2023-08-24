from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse

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


def generate_shopping_list_response(user):
    ingredients = (
        IngredientInRecipe.objects.select_related()
        .filter(recipe__shopping_cart__user=user)
        .order_by("ingredient__name")
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(amount=Sum("amount"))
    )

    shopping_list_buffer = create_shopping_list_file(ingredients)

    response = HttpResponse(
        shopping_list_buffer,
        content_type="text/plain",
    )
    response["Content-Disposition"] = "attachment; filename=pipi.txt"
    return response
