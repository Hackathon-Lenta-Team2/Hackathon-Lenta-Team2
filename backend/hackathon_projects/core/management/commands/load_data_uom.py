from csv import DictReader
from django.core.management import BaseCommand
from products.models import UOM


class Command(BaseCommand):
    """Класс добавления маркера UOM из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading product data")

        for row in DictReader(open('pr_df.csv')):
            id = row['pr_uom_id']

            if id == 1:
                uom = UOM(id=id, title='шт')
            else:
                uom = UOM(id=id, title='гр')
            uom.save()
