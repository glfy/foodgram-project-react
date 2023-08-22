from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.validators import slug_validator

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название тега",
        db_index=True,
    )
    color = models.CharField(
        max_length=7, blank=True, verbose_name="Цвет в HEX"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Уникальный слаг",
        validators=[slug_validator],
        db_index=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название ингредиента",
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единицы измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        unique_together = ["name", "measurement_unit"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="recipes",
    )
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="recipes/images/", verbose_name="Картинка"
    )
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Список ингредиентов",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="Список тегов", related_name="recipes"
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (в минутах)"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        indexes = [models.Index(fields=["name"])]
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель связи ингредиента и рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_quantities",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredientinrecipe",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="unique_ingredient"
            )
        ]

    def __str__(self):
        return f"""{self.amount} {self.ingredient.measurement_unit} of
                    {self.ingredient.name} in {self.recipe.name}"""
