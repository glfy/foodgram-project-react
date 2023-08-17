import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Import Ingridients data to database"

    def load_ingridient(self):
        with open(
            "data/ingredients.csv", newline="", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                obj, created = Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1]
                )
                if not created:
                    self.stdout.write(
                        self.style.WARNING(
                            f"""Ingridient {obj} already exists.
                            Skipping."""
                        )
                    )

    def handle(self, *args, **options):
        self.load_ingridient()
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
