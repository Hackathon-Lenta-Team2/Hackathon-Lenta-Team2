from csv import DictReader
from django.core.management import BaseCommand
from products.models import Group, Category


class Command(BaseCommand):
    """Класс добавления категорий из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading product data")

        for row in DictReader(open('pr_df.csv')):
            group_id = row['pr_group_id']
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                print(f"Category with ID {group_id} does not exist. Skipping.")
                continue

            category = Category(id=row['pr_cat_id'], group_id=group)
            category.save()
