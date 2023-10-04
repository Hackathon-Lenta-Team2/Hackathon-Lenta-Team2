from csv import DictReader
from django.core.management import BaseCommand
from products.models import Category, Subcategory


class Command(BaseCommand):
    """Класс добавления подкатегорий из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading product data")

        for row in DictReader(open('pr_df.csv')):
            category_id = row['pr_cat_id']
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                print(
                    f"Subcategory with ID {category_id} does not exist. Skipping.")
                continue

            category = Subcategory(
                id=row['pr_subcat_id'], category_id=category)
            category.save()
#