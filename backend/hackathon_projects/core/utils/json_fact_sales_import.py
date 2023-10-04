from csv import DictReader
from dataclasses import dataclass
from datetime import date, datetime

from loguru import logger

from products.models import StockKeepingUnit
from sales.models import FactSalesFile, Sale, SaleInfo
from stores.models import Store


@dataclass
class RowData:
    """Информация, полученная из ряда csv файла."""

    st_id: str
    pr_sku_id: str
    date: date
    sales_in_units: float
    promo_sales_in_units: float
    sales_in_rub: float
    promo_sales_in_rub: float


class FactSalesImportFromCSV:
    """Класс импорта данных фактических продаж из CSV в БД."""

    LOGGER_INFO_STEP: int = 10
    BULK_CREATE_BATCH_SIZE: int = 500

    def __init__(self, file: FactSalesFile) -> None:
        self.__file_model: FactSalesFile = file
        self.__file_path: str = self.__file_model.file_path.path
        self.__count: int = 0
        self.__data_to_write: list = []

    def import_data(self) -> None:
        try:
            logger.info("Импорт данных начался.")
            for row in DictReader(open(self.__file_path)):
                self.__count += 1
                if self.__count % self.LOGGER_INFO_STEP == 0:
                    logger.info(f"Обрабатывается {self.__count} строка...")

                row_data = self.__read_csv_row(row)
                sale = self.__get_or_create_correct_sale(
                    row_data.st_id, row_data.pr_sku_id
                )
                sale_info = self.__build_sale_info_obj(row_data, sale)
                self.__data_to_write.append(sale_info)

                if len(self.__data_to_write) >= self.BULK_CREATE_BATCH_SIZE:
                    SaleInfo.objects.bulk_create(self.__data_to_write)
                    self.__data_to_write.clear()

            if self.__data_to_write:
                self.__create_sale_info()
            logger.info("Импорт данных завершён.")

        except (KeyError, Exception) as er:
            logger.error("Неверный формат CSV файла или введённых данных.")
            logger.error(f"Error: {er}")

        finally:
            self.__delete_file()

    @staticmethod
    def __get_or_create_correct_sale(st_id: str, pr_sku_id: str) -> Sale:
        store = Store.objects.get(id=st_id)
        sku = StockKeepingUnit.objects.get(id=pr_sku_id)
        sale, _ = Sale.objects.get_or_create(store_id=store, sku_id=sku)
        return sale

    @staticmethod
    def __read_csv_row(row: str) -> RowData:
        st_id = row["st_id"]
        pr_sku_id = row["pr_sku_id"]
        date = datetime.strptime(row["date"], "%Y-%m-%d")
        sales_in_units = float(row["pr_sales_in_units"])
        promo_sales_in_units = float(row["pr_promo_sales_in_units"])
        sales_in_rub = float(row["pr_sales_in_rub"])
        promo_sales_in_rub = float(row["pr_promo_sales_in_rub"])
        return RowData(
            st_id=st_id,
            pr_sku_id=pr_sku_id,
            date=date,
            sales_in_units=sales_in_units,
            promo_sales_in_units=promo_sales_in_units,
            sales_in_rub=sales_in_rub,
            promo_sales_in_rub=promo_sales_in_rub,
        )

    @staticmethod
    def __build_sale_info_obj(row_data: RowData, sale: Sale) -> SaleInfo:
        return SaleInfo(
            sale_id=sale,
            date=row_data.date,
            sales_type=(row_data.promo_sales_in_units > 0),
            sales_units=row_data.sales_in_units,
            sales_units_promo=row_data.promo_sales_in_units,
            sales_rub=row_data.sales_in_rub,
            sales_rub_promo=row_data.promo_sales_in_rub,
        )

    def __create_sale_info(self):
        SaleInfo.objects.bulk_create(self.__data_to_write)

    def __delete_file(self):
        self.__file_model.delete()
