import secrets

import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda x: x)
    password = (secrets.token_hex(16),)
    username = factory.Sequence(lambda n: "admin%s" % n)
    email = factory.Sequence(lambda n: "admin%s@mail.ru" % n)

    class Meta:
        model = User
        django_get_or_create = ("id", "password", "username")
