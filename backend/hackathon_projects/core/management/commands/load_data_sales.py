from csv import DictReader
from django.core.management import BaseCommand
from sales.models import Sale, SaleInfo
from products.models import StockKeepingUnit
from stores.models import Store
from datetime import datetime


class Command(BaseCommand):
    """Класс добавления продаж из CSV файла в БД."""

    def handle(self, *args, **options):
        print("Loading sales data")

        batch_size = 1000

        sale_list = []
        sale_info_list = []

        for row in DictReader(open('sales_df_train.csv')):
            st_id = row['st_id']
            pr_sku_id = row['pr_sku_id']
            date = datetime.strptime(row['date'], '%Y-%m-%d')
            sales_in_units = float(row['pr_sales_in_units'])
            promo_sales_in_units = float(row['pr_promo_sales_in_units'])
            sales_in_rub = float(row['pr_sales_in_rub'])
            promo_sales_in_rub = float(row['pr_promo_sales_in_rub'])

            store, _ = Store.objects.get_or_create(id=st_id)
            sku, _ = StockKeepingUnit.objects.get_or_create(id=pr_sku_id)

            sale = Sale(store_id=store, sku_id=sku)
            sale_list.append(sale)

            sale_info = SaleInfo(
                sale_id=sale,
                date=date,
                sales_type=(promo_sales_in_units > 0),
                sales_units=sales_in_units,
                sales_units_promo=promo_sales_in_units,
                sales_rub=sales_in_rub,
                sales_rub_promo=promo_sales_in_rub,
            )
            sale_info_list.append(sale_info)

            if len(sale_list) >= batch_size:
                Sale.objects.bulk_create(sale_list)
                SaleInfo.objects.bulk_create(sale_info_list)
                sale_list = []
                sale_info_list = []

        Sale.objects.bulk_create(sale_list)
        SaleInfo.objects.bulk_create(sale_info_list)

        print("Sales data loaded successfully")
