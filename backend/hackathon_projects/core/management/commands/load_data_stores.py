from csv import DictReader
from django.core.management import BaseCommand
from stores.models import City, Division, Format, Size, Location, Store


class Command(BaseCommand):
    """Класс добавления супермаркетов из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading stores data")

        for row in DictReader(open('st_df.csv')):
            city_id = row['st_city_id']
            format_id = row['st_type_format_id']
            div_id = row['st_division_code']
            loc_id = row['st_type_loc_id']
            size_id = row['st_type_size_id']
            try:
                city = City.objects.get(id=city_id)
                format = Format.objects.get(id=format_id)
                div = Division.objects.get(id=div_id)
                loc = Location.objects.get(id=loc_id)
                size = Size.objects.get(id=size_id)
            except Store.DoesNotExist:
                print(f"ID does not exist. Skipping.")
                continue

            store = Store(
                id=row['st_id'], city=city, division=div, type_format=format, loc=loc, size=size)
            store.save()
