from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from users.models import User


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
        print(self.context)
        user = self.context("request").user
        if user.is_anonymous:
            return False
        return user.subsctiptions.filter(id=object.id).exists()


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
