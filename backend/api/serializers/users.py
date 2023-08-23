from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Сериалайзер пользователя"""

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
        return Subscription.objects.filter(
            subscriber=user.id, subscribed_to=object.id
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериалайзер создания пользователя"""

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
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, object):
        user = self.context["request"].user
        if user.is_anonymous or (user == object):
            return False
        return Subscription.objects.filter(
            subscriber=user.id, subscribed_to=object.id
        ).exists()

    def get_recipes(self, object):
        from .recipe import \
            RecipeMinifiedSerializer  # Import here to avoid circular import

        serializer = RecipeMinifiedSerializer(
            object.recipes, many=True, read_only=True
        )
        return serializer.data

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
        read_only_fields = ("email", "username", "first_name", "last_name")
