from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import username_validator


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Адрес электронной почты"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Уникальный юзернейм",
        validators=[username_validator],
    )
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")

    subscriptions = models.ManyToManyField(
        "users.User",
        related_name="subscribers",
        verbose_name="Подписан ли текущий пользователь на этого",
        default=False,
        editable=False,
        blank=True,
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Пароль",
    )

    favorite_recipes = models.ManyToManyField(
        "recipes.Recipe",
        related_name="favorited_by_users",
        verbose_name="Избранные рецепты",
        blank=True,
    )

    shopping_cart = models.ManyToManyField(
        "recipes.Recipe",
        related_name="recipes_in_shopping_cart",
        verbose_name="Рецепты в корзине",
        default=False,
        editable=False,
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username[:15]
