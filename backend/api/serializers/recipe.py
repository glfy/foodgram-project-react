import base64

from rest_framework import serializers

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from core.validators import validate_ingredients
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)

from .users import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientinRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient"
    )
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientinRecipeSerializer(
        many=True, source="ingredient_quantities"
    )
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "is_favorited",
            "is_shopping_cart",
        )

    def get_is_favorited(self, object):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=object).exists()
        return False

    def get_is_in_shopping_cart(self, object):
        user = self.context["request"].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe=object
            ).exists()
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(write_only=True)
    ingredients = serializers.ListField(
        write_only=True, validators=[validate_ingredients]
    )
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

        read_only_fields = (
            "is_favorited",
            "is_shopping_cart",
        )

    def create(self, validated_data):
        tags_data: list[int] = validated_data.pop("tags")
        ingredients_data: dict[int, tuple] = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        tags = Tag.objects.filter(id__in=tags_data)
        recipe.tags.set(tags)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data["id"]

            amount = ingredient_data["amount"]
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)

            IngredientInRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        return recipe

    def to_representation(self, recipe):
        serializer = RecipeReadSerializer(
            recipe, context={"request": self.context.get("request")}
        )
        return serializer.data

    def get_is_favorited(self, object):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=object).exists()
        return False

    def get_is_in_shopping_cart(self, object):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=object).exists()
        return False

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        ingredients_data = validated_data.pop("ingredients", [])

        tags = Tag.objects.filter(id__in=tags_data)
        instance.tags.set(tags)

        instance.ingredient_quantities.all().delete()

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data["id"]
            amount = ingredient_data["amount"]
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            IngredientInRecipe.objects.create(
                recipe=instance, ingredient=ingredient, amount=amount
            )

        return super().update(instance, validated_data)


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
