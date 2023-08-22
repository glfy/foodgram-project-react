# Generated by Django 3.2.9 on 2023-08-21 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_unique_recipe_ingredients"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(
                db_index=True, max_length=200, verbose_name="Название ингредиента"
            ),
        ),
        migrations.AlterField(
            model_name="ingredientinrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredientinrecipe",
                to="recipes.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AlterField(
            model_name="ingredientinrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_quantities",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ingredient",
            unique_together={("name", "measurement_unit")},
        ),
    ]
