from csv import DictReader
from django.core.management import BaseCommand
from stores.models import Format


class Command(BaseCommand):
    """Класс добавления формата из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading format data")

        for row in DictReader(open('st_df.csv')):
            id = row['st_type_format_id']

            format = Format(id=id)
            format.save()
