import datetime
from datetime import datetime

from django.db.models.deletion import RestrictedError
from django.test import TestCase

from core.model_factories.forecast_factory import ForecastFactory
from core.model_factories.sku_factory import StockKeepingUnitFactory
from core.model_factories.store_factory import StoreFactory
from forecasts.models import Forecast, ForecastData
from products.models import StockKeepingUnit
from stores.models import Store


class ForecastModelTest(TestCase):
    """Класс тестов модели Forecast."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.sku: StockKeepingUnit = StockKeepingUnitFactory()
        cls.store: Store = StoreFactory()
        times = datetime.now().strftime("%Y-%m-%d")
        cls.forecast_date = times
        cls.forecast = Forecast.objects.create(
            store=cls.store,
            sku=cls.sku,
            forecast_date=cls.forecast_date
        )

    def test_object_was_created(self):
        self.assertEquals(Forecast.objects.count(), 1)

    def test_object_name_is_correct(self):
        object_name = f"Forecast_id: {self.forecast.id}"
        self.assertEqual(object_name, str(self.forecast))

    def test_correctly_verbose_name(self):
        field_verbose_name = {
            'store': 'Супермаркет',
            'sku': 'Товар',
            'forecast_date': 'Дата'
        }
        for fields, verbose_name in field_verbose_name.items():
            with self.subTest(fields=fields):
                self.assertEquals(
                    self.forecast._meta.get_field(fields).verbose_name,
                    verbose_name,
                )

    def test_deleting_work_correctly(self):
        for model in (
            self.sku,
            self.store,
        ):
            with self.subTest(model=model):
                self.assertRaises(RestrictedError, model.delete)


class ForecastDataModelTest(TestCase):
    """Класс тестов модели ForecastData."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.forecast: Forecast = ForecastFactory()
        data_json = {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
        cls.data = data_json
        cls.forecast_date = ForecastData.objects.create(
            forecast_id=cls.forecast,
            data=cls.data
        )

    def test_object_was_created(self):
        self.assertEquals(ForecastData.objects.count(), 1)

    def test_correctly_verbose_name(self):
        field_verbose_name = {
            'forecast_id': 'ID прогноза'
        }
        for fields, verbose_name in field_verbose_name.items():
            with self.subTest(fields=fields):
                self.assertEquals(
                    self.forecast_date._meta.get_field(fields).verbose_name,
                    verbose_name,
                )

    def test_deleting_work_correctly(self):
        for model in (
            self.forecast,
        ):
            with self.subTest(model=model):
                self.assertRaises(RestrictedError, model.delete)
