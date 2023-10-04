import secrets

import factory

from products.models import UOM, Category, Group, StockKeepingUnit, Subcategory


class GroupFactory(factory.django.DjangoModelFactory):
    id = secrets.token_hex(16)

    class Meta:
        model = Group
        django_get_or_create = ("id",)


class CategoryFactory(factory.django.DjangoModelFactory):
    id = secrets.token_hex(16)
    group_id = factory.SubFactory(GroupFactory)

    class Meta:
        model = Category
        django_get_or_create = ("id",)


class SubCategoryFactory(factory.django.DjangoModelFactory):
    id = secrets.token_hex(16)
    category_id = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Subcategory
        django_get_or_create = ("id",)


class UOMFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda x: x)

    class Meta:
        model = UOM
        django_get_or_create = ("id",)


class StockKeepingUnitFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda x: x)
    title = factory.Faker("name")
    group_id = factory.SubFactory(GroupFactory)
    cat_id = factory.SubFactory(CategoryFactory)
    subcat_id = factory.SubFactory(SubCategoryFactory)
    uom_id = factory.SubFactory(UOMFactory)

    class Meta:
        model = StockKeepingUnit
        django_get_or_create = ("id",)
