from csv import DictReader
from django.core.management import BaseCommand
from sales.models import Sale, SaleInfo
from datetime import datetime


class Command(BaseCommand):
    """Класс добавления продаж из CSV файла в БД."""

    def handle(self, *args, **options):
        sale_info_list = []
        batch_size = 2000

        print("Loading sales data")
        count = 0

        for row in DictReader(open("sales_df_train.csv")):
            count += 1
            if count % 10000 == 0:
                print(f"Now on {count} row.")

            st_id = row["st_id"]
            pr_sku_id = row["pr_sku_id"]
            date = datetime.strptime(row["date"], "%Y-%m-%d")
            sales_in_units = float(row["pr_sales_in_units"])
            promo_sales_in_units = float(row["pr_promo_sales_in_units"])
            sales_in_rub = float(row["pr_sales_in_rub"])
            promo_sales_in_rub = float(row["pr_promo_sales_in_rub"])

            sale = Sale.objects.get(store_id=st_id, sku_id=pr_sku_id)

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

            if len(sale_info_list) >= batch_size:
                SaleInfo.objects.bulk_create(sale_info_list)
                sale_info_list.clear()

        if sale_info_list:
            SaleInfo.objects.bulk_create(sale_info_list)

        print("Sales data loaded successfully")
