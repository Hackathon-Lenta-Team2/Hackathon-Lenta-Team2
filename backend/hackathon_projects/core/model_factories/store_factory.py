import secrets

import factory

from stores.models import City, Division, Format, Location, Size, Store


class CityFactory(factory.django.DjangoModelFactory):
    id = secrets.token_hex(32)

    class Meta:
        model = City
        django_get_or_create = ("id",)


class DivisionFactory(factory.django.DjangoModelFactory):
    id = secrets.token_hex(32)

    class Meta:
        model = Division
        django_get_or_create = ("id",)


class FormatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Format


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location


class StoreFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda x: x)
    city = factory.SubFactory(CityFactory)
    division = factory.SubFactory(DivisionFactory)
    type_format = factory.SubFactory(FormatFactory)
    loc = factory.SubFactory(LocationFactory)
    size = factory.SubFactory(SizeFactory)

    class Meta:
        model = Store
        django_get_or_create = ("id",)
