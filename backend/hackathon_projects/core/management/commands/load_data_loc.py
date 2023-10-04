from csv import DictReader
from django.core.management import BaseCommand
from stores.models import Location


class Command(BaseCommand):
    """Класс добавления типа локации из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading location data")

        for row in DictReader(open('st_df.csv')):
            id = row['st_type_loc_id']

            loc = Location(id=id, type=f"Тип локации {id}")
            loc.save()
