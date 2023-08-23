from rest_framework import serializers

from django.core.validators import RegexValidator

slug_validator = RegexValidator(
    regex=r"^[-a-z0-9_]+$",
    message=(
        "Слаг должен состоять только из латинских букв нижнего регистра, "
        "цифр, дефисов и нижних подчеркиваний."
    ),
)

username_validator = RegexValidator(
    regex=r"^[\w.@+-]+$",
    message="""Имя пользователя должно состоять из букв, цифр или этих знаков:
    @ . + - _""",
)


def validate_ingredients(value_list):
    validated_ingredients = []

    for value in value_list:
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Ингредиенты должны быть переданы в формате"
                "{ингредиент: количество}"
            )
    ingredient_id = value.get("id")
    amount = value.get("amount")
    if ingredient_id is None or amount is None:
        raise serializers.ValidationError(
            "Каждый ингредиент должен иметь 'id' и 'amount'"
        )
    if int(amount) <= 0:
        raise serializers.ValidationError(
            "Количество ингредиента должно быть больше 0."
        )
    if "Ingredient" not in globals():
        from recipes.models import Ingredient
    if not Ingredient.objects.filter(id=ingredient_id).exists():
        raise serializers.ValidationError(
            f"Ингредиент с ID {ingredient_id} не существует"
        )
    validated_ingredients.append((ingredient_id, amount))
    return validated_ingredients
