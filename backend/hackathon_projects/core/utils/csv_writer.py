import itertools
from datetime import date, datetime, timedelta  # noqa

import pandas as pd
from django.conf import settings
from django.db.models import QuerySet, Sum
from typing_extensions import Any

from sales.models import Sale


class CSVWriter:
    """Класс для записи данных для DS в формате CSV файла.
    Для запуска используется метод write().
    """

    # последние данные по продажам есть на 18-07-2023
    RESEARCH_DAY: date = date(year=2023, month=7, day=18)

    # для запуска на реальную дату использовать
    # RESEARCH_DAY: date = datetime.today().date()

    def __init__(self) -> None:
        self.__file_name = settings.DATA_FILES_DIR / "ds_data.csv"
        self.__rows_to_write = []
        self.__date_now = self.RESEARCH_DAY

    def write(self):
        """Выгрузить данные продаж из БД в файл."""
        self.__populate_rows_to_write_with_db_data()
        self.__write_csv_file()

    @staticmethod
    def __get_sales_in_days_dict(
        sale_info: QuerySet[dict[str, Any]]
    ) -> dict[str, float | None]:
        """Возвращает словарь данных lag_N: Количество продаж."""

        sales_in_dates = [str(f"lag_{x}") for x in range(22)]
        values = [float(entry["sum_sales_units"]) for entry in sale_info]
        # values м.б. короче чем sales_in_dates
        # заполнит недостающие значения lags - None
        combs = [
            comb for comb in itertools.zip_longest(sales_in_dates, values)
        ]
        sales_in_dates = {k: v for k, v in combs}

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

    @staticmethod
    def __get_sale_info(sale: Sale) -> QuerySet[dict[str, Any]]:
        """
        Возвращает отфильтрованные данные таблицы SaleInfo.
        Группирует продажи по дате.
        Суммирует количество продаж в один день.
        """

        return (
            sale.sale_info.values("date")
            .annotate(sum_sales_units=Sum("sales_units"))
            .order_by("-date")
            .filter(sum_sales_units__gt=0)[:22]
        )

    @staticmethod
    def __get_sales() -> QuerySet[Sale]:
        """Возвращает данные таблицы Sale."""
        return Sale.objects.all().select_related("store_id", "sku_id")

    def __populate_rows_to_write_with_db_data(self) -> None:
        """Добавляет в rows_to_write отдельные записи с данными."""
        sales = self.__get_sales()
        for sale in sales:
            sale_info = self.__get_sale_info(sale)
            if sale_info:
                sales_in_days = self.__get_sales_in_days_dict(sale_info)
                row = self.__get_row_base_info(sale)
                # добавить записи lag_0 - lag_21
                row.update(sales_in_days)
                self.__rows_to_write.append(row)

    def __write_csv_file(self) -> None:
        """Пишет rows_to_write в CSV файл."""
        lines = pd.DataFrame(self.__rows_to_write)
        # "-" где нет данных
        lines.to_csv(self.__file_name, index=False, na_rep="-")
