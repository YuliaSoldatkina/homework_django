import json
from django.core.management.base import BaseCommand
from django.core.management import call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур, предварительно очищая базу"

    def handle(self, *args, **options):
        # Удаляем все данные
        self.stdout.write("Удаление существующих данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем фикстуры
        self.stdout.write("Загрузка фикстур...")
        call_command("loaddata", "fixtures/catalog_data.json")

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))