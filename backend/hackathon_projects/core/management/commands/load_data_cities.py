from csv import DictReader
from django.core.management import BaseCommand
from stores.models import City


class Command(BaseCommand):
    """Класс добавления городов из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading city data")

        for row in DictReader(open('st_df.csv')):
            id = row['st_city_id']

            city = City(id=id)
            city.save()
#