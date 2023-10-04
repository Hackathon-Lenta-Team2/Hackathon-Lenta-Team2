from csv import DictReader
from django.core.management import BaseCommand
from stores.models import Group


class Command(BaseCommand):
    """Класс добавления городов из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading group data")

        for row in DictReader(open('pr_df.csv')):
            id = row['pr_group_id']

            group = Group(id=id)
            group.save()
