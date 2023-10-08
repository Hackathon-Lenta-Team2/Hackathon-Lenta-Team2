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

        cls.user = UserFactory()
        cls.token = Token.objects.create(user=cls.user)

    def user_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
