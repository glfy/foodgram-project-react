from rest_framework import serializers
from recipes.models import Tag, IngredientInRecipe, Recipe, Ingredient
from .users import CustomUserSerializer
from django.db.models import F
from core.validators import validate_ingridients
import base64
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status


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
        fields = "__all__"
        read_only_fields = ("__all__",)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


# class IngredientInRecipeSerializer(serializers.ModelSerializer):
#     ingredient = IngredientSerializer(source="*")

#     class Meta:
#         model = IngredientInRecipe
#         fields = ["ingredient", "amount"]


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = obj.ingredient_quantities.all()
        serialized_ingredients = [
            {
                "id": ingredient.ingredient.id,
                "name": ingredient.ingredient.name,
                "measurement_unit": ingredient.ingredient.measurement_unit,
                "amount": ingredient.amount,
            }
            for ingredient in ingredients
        ]
        return serialized_ingredients

    def get_tags(self, obj):
        return [
            {
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "slug": tag.slug,
            }
            for tag in obj.tags.all()
        ]

    def get_is_favorited(self, obj):
        user = self.context["request"].user

        if user.is_authenticated:
            print(obj.favorited_by_users.all())
            return obj.favorited_by_users.filter(id=user.id).exists()
        return False

    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context["request"].user
    #     if user.is_authenticated:
    #         return obj.shopping_cart.filter(user=user).exists()
    #     return False

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "is_favorited",
            # "is_shopping_cart",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(write_only=True)
    ingredients = serializers.ListField(
        write_only=True, validators=[validate_ingridients]
    )
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

        read_only_fields = (
            "is_favorited",
            # "is_shopping_cart",
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
            ingredient = Ingredient.objects.get(id=ingredient_id)

            IngredientInRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )

        return recipe

    def to_representation(self, recipe):
        serializer = RecipeReadSerializer(
            recipe, context={"request": self.context.get("request")}
        )

        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context["request"].user

        if user.is_authenticated:
            print(obj.favorited_by_users.all())
            return obj.favorited_by_users.filter(id=user.id).exists()
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
            ingredient = Ingredient.objects.get(id=ingredient_id)

            IngredientInRecipe.objects.create(
                recipe=instance, ingredient=ingredient, amount=amount
            )

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            return instance

    @action(
        detail=True, methods=["delete"], permission_classes=[IsAuthenticated]
    )
    def delete_recipe(self, request, pk=None):
        recipe = self.instance
        if recipe.author == request.user or request.user.is_staff:
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "detail": "Этот рецепт не принадлежит вам и вы не"
                    "администратор, поэтому вы не можете удалить его."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
