from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from api.tests.test_utils import BaseUserTest

User = get_user_model()


class URLsTest(BaseUserTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.list_urls = [
            reverse("api:cities-list"),
            reverse("api:divisions-list"),
            reverse("api:formats-list"),
            reverse("api:stores-list"),
            reverse("api:products-list"),
            reverse("api:forecasts-list"),
            reverse("api:profile"),
            reverse("api:groups-list"),
            reverse("api:categories-list"),
            reverse("api:subcategories-list"),
        ]

    def test_list_urls_unauthorized_prohibited(self):
        self.client.credentials()
        for url in self.list_urls:
            with self.subTest(url):
                response = self.client.get(url, format="json")
                self.assertEqual(
                    response.status_code, status.HTTP_401_UNAUTHORIZED
                )

    def test_sales_url_unauthorized_prohibited(self):
        self.client.credentials()
        url = reverse("api:sales-list")
        payload = {"store": "123", "sku": "123"}
        response = self.client.get(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_urls_authorized_work_correctly(self):
        self.user_authorization()
        for url in self.list_urls:
            with self.subTest(url):
                response = self.client.get(url, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sales_url_authorized_works_correctly(self):
        self.user_authorization()
        url = reverse("api:sales-list")
        payload = {"store": "123", "sku": "123"}
        response = self.client.get(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
