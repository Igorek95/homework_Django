from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Fill data in the database'

    def handle(self, *args, **options):
        Category.objects.all().delete()

        Category.objects.create(name="Фрукты", description="Разнообразные фрукты")
        Category.objects.create(name="Овощи", description="Различные виды овощей")

        self.stdout.write(self.style.SUCCESS('Data has been filled successfully'))
