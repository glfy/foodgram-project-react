# Generated by Django 3.2.9 on 2023-08-22 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_subscription_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorite_recipes',
        ),
    ]
