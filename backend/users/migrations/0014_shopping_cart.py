# Generated by Django 3.2.9 on 2023-08-23 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='shopping_cart',
        ),
    ]