# Generated by Django 3.2.9 on 2023-08-22 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]