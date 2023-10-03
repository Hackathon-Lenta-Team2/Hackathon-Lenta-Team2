import secrets

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class BaseUserTest(APITestCase):
    """Класс создания пользователя для Тестов."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create(
            username="admin",
            password=secrets.token_hex(16),
            email="admin@mail.ru",
        )

        cls.token = Token.objects.create(user=cls.user)

    def create_token(self):
        return self.token

    def user_authorization(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.create_token().key)
