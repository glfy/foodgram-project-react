from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser if it does not exist"

    def handle(self, *args, **options):
        username = "admin"
        email = "a@a.ru"
        password = "admin"

        if not User.objects.filter(
            username=username, is_superuser=True
        ).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS("Superuser created successfully")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
