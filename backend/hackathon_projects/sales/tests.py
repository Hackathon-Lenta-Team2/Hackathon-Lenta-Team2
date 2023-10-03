from datetime import datetime

from django.test import TestCase

from core.model_factories.sale_factory import SaleFactory
from core.model_factories.sku_factory import StockKeepingUnitFactory
from core.model_factories.store_factory import StoreFactory
from products.models import StockKeepingUnit
from sales.models import Sale, SaleInfo
from stores.models import Store


class SaleModelTests(TestCase):
    """Класс тестов модели Sale."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.store = StoreFactory()
        cls.sku = StockKeepingUnitFactory()

        cls.sale: Sale = Sale.objects.create(
            store_id=cls.store, sku_id=cls.sku
        )

    def test_object_was_created(self):
        self.assertEquals(Sale.objects.count(), 1)

    def test_fields_has_correct_type(self):
        self.assertIsInstance(self.sale.id, int)
        self.assertIsInstance(self.sale.store_id, Store)
        self.assertIsInstance(self.sale.sku_id, StockKeepingUnit)

    def test_sale_object_name_is_correct(self):
        expected_object_name = (
            f"Sale: id={self.sale.id}, store_id={self.store}, "
            f"sku_id={self.sku}"
        )
        self.assertEqual(expected_object_name, str(self.sale))

    def test_relations_work_correctly(self):
        for model in (self.store, self.sku):
            with self.subTest(model=model):
                self.assertEquals(model.sales.count(), 1)
                self.assertEquals(model.sales.first(), self.sale)

    def test_store_fields_has_correct_verbose_names(self):
        field_verbose_name: dict = {
            "store_id": "Супермаркет",
            "sku_id": "Товар",
        }
        for field, verbose_name in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.sale._meta.get_field(field).verbose_name,
                    verbose_name,
                )


class SaleInfoModelTests(TestCase):
    """Класс тестов модели SaleInfo."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sale = SaleFactory()
        cls.sale_info: SaleInfo = SaleInfo.objects.create(
            sale_id=cls.sale,
            date=datetime.utcnow(),
            sales_type=True,
            sales_units=123.5,
            sales_units_promo=123.2,
            sales_rub=123.6,
            sales_rub_promo=123.9,
        )

    def test_object_was_created(self):
        self.assertEquals(SaleInfo.objects.count(), 1)

    def test_fields_has_correct_type(self):
        fields_instances = {
            self.sale_info.sale_id: Sale,
            self.sale_info.date: datetime,
            self.sale_info.sales_type: bool,
            self.sale_info.sales_units: float,
            self.sale_info.sales_units_promo: float,
            self.sale_info.sales_rub: float,
            self.sale_info.sales_rub_promo: float,
        }
        for field, instance in fields_instances.items():
            with self.subTest(field=field):
                self.assertIsInstance(
                    field, instance, msg=f"{field} - {instance}"
                )

    def test_sale_info_object_name_is_correct(self):
        expected_object_name = (
            f"SaleInfo: id={self.sale_info.id}, sale_id={self.sale}, "
            f"date={self.sale_info.date}"
        )
        self.assertEqual(expected_object_name, str(self.sale_info))

    def test_relation_works_correctly(self):
        self.assertEquals(self.sale.sale_info.count(), 1)
        self.assertEquals(self.sale.sale_info.first(), self.sale_info)

    def test_store_fields_has_correct_verbose_names(self):
        field_verbose_name: dict = {
            "sale_id": "Продажа",
            "date": "Дата продажи",
            "sales_type": "Флаг наличия промо",
            "sales_units": "Число проданных товаров без признака промо",
            "sales_units_promo": "Число проданных товаров с признаком промо",
            "sales_rub": "Продажи без признака промо в рублях",
            "sales_rub_promo": "Продажи с признаком промо в рублях",
        }
        for field, verbose_name in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.sale_info._meta.get_field(field).verbose_name,
                    verbose_name,
                )
