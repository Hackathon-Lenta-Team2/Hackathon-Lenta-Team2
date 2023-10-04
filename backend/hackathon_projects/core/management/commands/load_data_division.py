from csv import DictReader
from django.core.management import BaseCommand
from stores.models import Division


class Command(BaseCommand):
    """Класс добавления дивизиона из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading division data")

        for row in DictReader(open("st_df.csv")):
            id = row["st_division_code"]

            div = Division(id=id)
            div.save()
#