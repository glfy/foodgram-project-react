from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from users.models import User
from rest_framework.fields import CurrentUserDefault


class CustomUserSerializer(UserSerializer):
    """
    Serializer for User model.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, object):
        user = self.context["request"].user
        if user.is_anonymous or (user == object):
            return False
        return user.subscriptions.filter(id=object.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for user registration.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    def get_recipes_count(self, user):
        return user.recipes.count()

    def recipes_serializer(self, user):
        """
        Dynamic import to avoid circular import.

        """
        from .recipe import RecipeMinifiedSerializer

        subscribed_recipes = user.recipes.all()

        return RecipeMinifiedSerializer(
            instance=subscribed_recipes,
            many=True,
            read_only=True,
            context=self.context,
        )

    def get_recipes(self, user):
        serializer = self.recipes_serializer(user)
        return serializer.data

    # subscriptions = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=get_user_model().objects.all()
    # )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
