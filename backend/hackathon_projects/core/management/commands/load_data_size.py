from csv import DictReader
from django.core.management import BaseCommand
from stores.models import Size


class Command(BaseCommand):
    """Класс добавления размера из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading size data")

        for row in DictReader(open("st_df.csv")):
            id = row["st_type_size_id"]

            size = Size(id=id, type=f"Тип размера {id}")
            size.save()
