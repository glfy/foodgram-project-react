from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = "Create tags which are used for recipe creation"

    def handle(self, *args, **options):
        Tag.objects.get_or_create(
            name="breakfast",
            slug="breakfast",
            color="#7FFFD4",
        )
        Tag.objects.get_or_create(name="lunch", slug="lunch", color="#F19CBB")
        Tag.objects.get_or_create(
            name="dinner", slug="dinner", color="#ABCDEF"
        )
