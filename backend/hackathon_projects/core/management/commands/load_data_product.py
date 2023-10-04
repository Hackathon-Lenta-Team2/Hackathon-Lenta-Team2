from csv import DictReader
from django.core.management import BaseCommand
from products.models import Group, Category, Subcategory, StockKeepingUnit, UOM


class Command(BaseCommand):
    """Класс добавления продуктов из csv файла в БД."""

    def handle(self, *args, **options):
        print("Loading product data")

        for row in DictReader(open('pr_df.csv')):
            group_id = row['pr_group_id']
            category_id = row['pr_cat_id']
            subcat_id = row['pr_subcat_id']
            uom_id = row['pr_uom_id']
            try:
                group = Group.objects.get(id=group_id)
                category = Category.objects.get(id=category_id)
                subcat = Subcategory.objects.get(id=subcat_id)
                uom = UOM.objects.get(id=uom_id)
            except Category.DoesNotExist:
                print(f"ID does not exist. Skipping.")
                continue

            product = StockKeepingUnit(
                id=row['pr_sku_id'], group_id=group, cat_id=category, subcat_id=subcat, uom_id=uom)
            product.save()
