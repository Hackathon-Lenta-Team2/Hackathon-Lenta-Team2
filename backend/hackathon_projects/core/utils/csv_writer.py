from datetime import date, datetime, timedelta

from django.conf import settings
import pandas as pd
from django.db.models import QuerySet
from typing_extensions import Any

from sales.models import Sale, SaleInfo


class CSVWriter:
    """Класс для записи данных для DS в формате CSV файла.
    Для запуска используется метод write().
    """

    def __init__(self) -> None:
        self.__file_name = settings.DATA_FILES_DIR / "ds_data.csv"
        self.__rows_to_write = []
        self.__date_now = datetime.today().date()
        self.__date_21_before = self.__get_date_some_range_before(21)

    def write(self):
        """Выгрузить данные продаж из БД в файл."""
        self.__populate_rows_to_write_with_db_data()
        self.__write_csv_file()

    def __get_date_some_range_before(self, days_range: int) -> date:
        """Возвращает дату с переданным смещением назад в днях."""
        return self.__date_now - timedelta(days=days_range)

    def __get_sales_in_days_dict(
        self, sale_info: QuerySet[SaleInfo]
    ) -> dict[str, float]:
        """Возвращает словарь данных Дата: Количество продаж."""

        sales_in_dates = {
            str(self.__get_date_some_range_before(x)): 0.0
            for x in range(21, 0, -1)
        }
        for sale in sale_info:
            sales_in_dates[str(sale.date)] += float(sale.sales_units)

        return sales_in_dates

    def __get_row_base_info(self, sale: Sale) -> dict[str, Any]:
        """Возвращает словарь данных, полученных из таблицы Sale."""
        return {
            "date_today": self.__date_now,
            "store_id": sale.store_id_id,
            "pr_sku_id": sale.sku_id_id,
            # products
            "pr_group_id": sale.sku_id.group_id_id,
            "pr_cat_id": sale.sku_id.cat_id_id,
            "pr_subcat_id": sale.sku_id.subcat_id_id,
            "pr_uom_id": sale.sku_id.uom_id_id,
            # stores
            "st_city_id": sale.store_id.city_id,
            "st_division_code": sale.store_id.division_id,
            "st_type_format_id": sale.store_id.type_format_id,
            "st_type_loc_id": sale.store_id.loc_id,
            "st_type_size_id": sale.store_id.size_id,
        }

    def __get_sale_info(self, sale: Sale) -> QuerySet[SaleInfo | None]:
        """
        Возвращает отфильтрованные данные таблицы SaleInfo.
        Фильтрует данные, относящиеся к одной продаже,
        в диапазоне последних 21 дней.
        """

        return sale.sale_info.filter(
            date__lt=self.__date_now, date__gte=self.__date_21_before
        ).order_by("date")

    def __populate_rows_to_write_with_db_data(self) -> None:
        """Добавляет в rows_to_write отдельные записи с данными."""
        sales = Sale.objects.all()
        for sale in sales:
            sale_info = self.__get_sale_info(sale)
            if sale_info:
                sales_in_days = self.__get_sales_in_days_dict(sale_info)
                row = self.__get_row_base_info(sale)
                row.update(sales_in_days)
                self.__rows_to_write.append(row)

    def __write_csv_file(self) -> None:
        """Пишет rows_to_write в CSV файл."""
        lines = pd.DataFrame(self.__rows_to_write)
        lines.to_csv(self.__file_name, index=False)
