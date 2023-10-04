from csv import DictReader
from django.core.management import BaseCommand
from sales.models import Sale
from products.models import StockKeepingUnit
from stores.models import Store


class Command(BaseCommand):
    """Класс добавления продаж из CSV файла в БД."""

    def handle(self, *args, **options):
        print("Loading sales data")
        count = 0
        for row in DictReader(open("sales_df_train.csv")):
            count += 1
            if count % 10000 == 0:
                print(f"Now on {count} row.")
            st_id = row["st_id"]
            pr_sku_id = row["pr_sku_id"]

            store = Store.objects.get(id=st_id)
            sku = StockKeepingUnit.objects.get(id=pr_sku_id)
            sale, _ = Sale.objects.get_or_create(store_id=store, sku_id=sku)

        print("Sales data loaded successfully")
