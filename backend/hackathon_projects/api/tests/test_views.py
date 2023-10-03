import json
import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from api.v_1.serializers.forecasts_serializers import JSONFileSerializer
from api.v_1.views.forecasts_views import ImportDataView
from core.create_user import BaseUserTest
from core.model_factories.sku_factory import (CategoryFactory, GroupFactory,
                                              StockKeepingUnitFactory,
                                              SubCategoryFactory)
from core.model_factories.store_factory import CityFactory, StoreFactory
from forecasts.models import Forecast, ForecastData
from products.models import StockKeepingUnit

User = get_user_model()


class StoresViewsTest(BaseUserTest):
    """Класс тестов возвращаемых данных модели Store."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.store = StoreFactory()
        cls.urls = [
            reverse("api:cities-list"),
            reverse("api:divisions-list"),
            reverse("api:formats-list"),
            reverse("api:stores-list"),
        ]

    def setUp(self) -> None:
        self.user_authorization()

    def test_stores_response_data_correct(self):
        data = {
            "id": str(self.store.id),
            "title": self.store.title,
            "is_active": self.store.is_active,
            "city": self.store.city.id,
            "division": self.store.division.id,
            "type_format": self.store.type_format.id,
            "loc": self.store.loc.id,
            "size": self.store.size.id,
        }
        response: Response = self.client.get(
            reverse("api:stores-list"), format="json"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], data)

    def test_search_works_correctly(self):
        city = CityFactory(id="123123123sad", title="Moscow")
        store_1 = StoreFactory(city=city)
        response = self.client.get(
            reverse("api:stores-list"), {"search": "Moscow"}
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], store_1.city.id)


class ImportDataViewTestCase(BaseUserTest):
    """Класс тестов вью-класса ImportDataView."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.store = StoreFactory()
        cls.sku = StockKeepingUnitFactory()
        cls.url = reverse("api:import-data")

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user_authorization()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_import_data_success(self):
        data_for_json = {
            "data": [
                {
                    "store": self.store.id,
                    "forecast_date": "2023-09-01",
                    "forecast": {
                        "sku": self.sku.id,
                        "sales_units": {
                            "2023-09-01": 0,
                        },
                    },
                },
            ]
        }
        json_data = json.dumps(data_for_json)
        json_file = SimpleUploadedFile(
            "forecast.json",
            bytes(json_data, encoding="utf-8"),
            content_type="application/json",
        )
        response = self.client.post(
            self.url, {"file": json_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"message": "Данные успешно импортированы"}
        )
        forecast = Forecast.objects.first()
        self.assertIsNotNone(forecast)
        self.assertEqual(forecast.store_id, str(self.store.id))
        self.assertEqual(forecast.sku_id, str(self.sku.id))
        self.assertEqual(str(forecast.forecast_date), "2023-09-01")

        forecast_data = ForecastData.objects.first()
        self.assertIsNotNone(forecast_data)
        self.assertEqual(forecast_data.forecast_id, forecast)
        self.assertEqual(forecast_data.data, {"2023-09-01": 0})

    def test_import_uncorrected_data(self):
        data_for_json = {
            "data": [
                {
                    "store": self.store.id,
                    "forecast": {
                        "sku": self.sku.id,
                        "sales_units": {
                            "2023-09-01": 0,
                        },
                    },
                },
            ]
        }
        json_data = json.dumps(data_for_json)
        json_file = SimpleUploadedFile(
            "forecast.json",
            bytes(json_data, encoding="utf-8"),
            content_type="application/json",
        )
        response = self.client.post(
            self.url, {"file": json_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_import_data_with_path(self):
        data_for_json = {
            "data": [
                {
                    "store": self.store.id,
                    "forecast_date": "2023-09-01",
                    "forecast": {
                        "sku": self.sku.id,
                        "sales_units": {
                            "2023-09-01": 0,
                        },
                    },
                },
            ]
        }
        json_data = json.dumps(data_for_json)
        temp_json_file_path = 'forecast_archive.json'
        temp_json_file_dir = 'data'
        self.temp_file_path = os.path.join(
            temp_json_file_dir, temp_json_file_path)
        with open(self.temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(json_data)
        response = self.client.post(
            reverse("api:import-data"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        forecast = Forecast.objects.first()
        self.assertIsNotNone(forecast)
        self.assertEqual(forecast.store_id, str(self.store.id))
        self.assertEqual(forecast.sku_id, str(self.sku.id))
        self.assertEqual(str(forecast.forecast_date), "2023-09-01")

        forecast_data = ForecastData.objects.first()
        self.assertIsNotNone(forecast_data)
        self.assertEqual(forecast_data.forecast_id, forecast)
        self.assertEqual(forecast_data.data, {"2023-09-01": 0})
        os.remove(self.temp_file_path)

    def test_import_data_error(self):
        json_file = SimpleUploadedFile("forecast.json", bytes(
            '{"invalid_json": "data"}', encoding="utf-8"), content_type="application/json")
        response = self.client.post(
            '/api/v1/import-data/', {'file': json_file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class StockKeepingUnitViewsTest(BaseUserTest):
    """Класс тестов возвращаемых данных модели Store."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.sku = StockKeepingUnitFactory()
        cls.urls = [
            reverse("api:groups-list"),
            reverse("api:categories-list"),
            reverse("api:subcategories-list"),
            reverse("api:products-list"),
        ]

    def setUp(self) -> None:
        self.user_authorization()

    def test_stores_response_data_correct(self):
        data = {
            "id": str(self.sku.id),
            "title": self.sku.title,
            "group_id": self.sku.group_id.id,
            "cat_id": self.sku.cat_id.id,
            "subcat_id": self.sku.subcat_id.id,
            "uom_id": self.sku.uom_id.id,
        }
        response: Response = self.client.get(
            reverse("api:products-list"), format="json"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], data)

    def test_filter_works_correctly(self):
        subcat = SubCategoryFactory(id="123123123sad")
        store_1 = StockKeepingUnitFactory(subcat_id=subcat)
        filter_params = {"subcat_id": subcat.id}
        response = self.client.get(
            reverse("api:products-list"),
            data=filter_params,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["subcat_id"], subcat.id)


class GroupViewsTest(BaseUserTest):
    """Класс тестов возвращаемых данных модели Group."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.group = GroupFactory()
        cls.urls = [
            reverse("api:groups-list"),
        ]

    def setUp(self) -> None:
        self.user_authorization()

    def test_stores_response_data_correct(self):
        data = {
            "id": str(self.group.id),
        }
        response: Response = self.client.get(
            reverse("api:groups-list"), format="json"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], data)


class CategoryViewsTest(BaseUserTest):
    """Класс тестов возвращаемых данных модели Category."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.category = CategoryFactory()
        cls.urls = [
            reverse("api:categories-list")
        ]

    def setUp(self) -> None:
        self.user_authorization()

    def test_stores_response_data_correct(self):
        data = {
            "id": str(self.category.id),
            "group_id": str(self.category.group_id.id),
        }
        response: Response = self.client.get(
            reverse("api:categories-list"), format="json"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], data)

    def test_filter_works_correctly(self):
        group = GroupFactory()
        category = CategoryFactory(group_id=group)
        filter_params = {"group_id": group.id}
        response = self.client.get(
            reverse("api:categories-list"),
            data=filter_params,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["group_id"], group.id)


class SubcategoryViewsTest(BaseUserTest):
    """Класс тестов возвращаемых данных модели Subcategory."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.subcategory = SubCategoryFactory()
        cls.urls = [
            reverse("api:subcategories-list")
        ]

    def setUp(self) -> None:
        self.user_authorization()

    def test_stores_response_data_correct(self):
        data = {
            "id": str(self.subcategory.id),
            "category_id": str(self.subcategory.category_id.id),
        }
        response: Response = self.client.get(
            reverse("api:subcategories-list"), format="json"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], data)

    def test_filter_works_correctly(self):
        category = CategoryFactory()
        subcategory = SubCategoryFactory(category_id=category)
        filter_params = {"category_id": category.id}
        response = self.client.get(
            reverse("api:subcategories-list"),
            data=filter_params,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["category_id"], category.id)
