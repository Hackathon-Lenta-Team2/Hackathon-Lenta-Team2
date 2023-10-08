from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from api.tests.test_utils import BaseUserTest
from core.model_factories.sku_factory import (CategoryFactory, GroupFactory,
                                              StockKeepingUnitFactory,
                                              SubCategoryFactory)
from core.model_factories.store_factory import CityFactory, StoreFactory

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
