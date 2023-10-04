import secrets

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.model_factories.user_factory import UserFactory

User = get_user_model()


class BaseUserTest(APITestCase):
    """Класс создания пользователя для Тестов."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # cls.user = User.objects.create(
        #     username="admin1",
        #     password=secrets.token_hex(16),
        #     email="admin1@mail.ru",
        # )
        cls.user = UserFactory()
        cls.token = Token.objects.create(user=cls.user)

    def create_token(self):
        return self.token

    def user_authorization(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.create_token().key)
