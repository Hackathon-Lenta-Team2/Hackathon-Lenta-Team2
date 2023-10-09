import random
import secrets

from django.db.models.deletion import RestrictedError
from django.test import TestCase

from core.model_factories.sku_factory import (
    CategoryFactory,
    GroupFactory,
    SubCategoryFactory,
    UOMFactory,
)

from .models import UOM, Category, Group, StockKeepingUnit, Subcategory


class GroupModelTest(TestCase):
    """Класс тестов модели Group."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.id = secrets.token_hex(16)
        cls.group = Group.objects.create(id=cls.id)

    def test_object_was_created(self):
        self.assertEquals(Group.objects.count(), 1)

    def test_id_field_has_correct_type(self):
        self.assertIsInstance(self.group.id, str)

    def test_id_field_has_correct(self):
        self.assertEqual(self.group.id, self.id)

    def test_object_name_is_correct(self):
        object_name = f"Group: id={self.id}"
        self.assertEqual(object_name, str(self.group))


class CategoryModelTest(TestCase):
    """Класс тестов модели Category."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.group_id = secrets.token_hex(16)
        cls.group = Group.objects.create(id=cls.group_id)

        cls.id = secrets.token_hex(16)
        cls.category = Category.objects.create(id=cls.id, group_id=cls.group)

    def test_object_was_created(self):
        self.assertEquals(Category.objects.count(), 1)

    def test_id_field_has_correct_type(self):
        self.assertIsInstance(self.category.id, str)

    def test_id_field_has_correct(self):
        self.assertEqual(self.category.id, self.id)

    def test_object_name_is_correct(self):
        object_name = f"Category: id={self.id}"
        self.assertEqual(object_name, str(self.category))


class SubcategoryModelTest(TestCase):
    """Класс тестов модели Subcategory."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.group_id = secrets.token_hex(16)
        cls.group = Group.objects.create(id=cls.group_id)

        cls.category_id = secrets.token_hex(16)
        cls.category = Category.objects.create(
            id=cls.category_id, group_id=cls.group
        )

        cls.id = secrets.token_hex(16)
        cls.subcategory = Subcategory.objects.create(
            id=cls.id, category_id=cls.category
        )

    def test_id_field_has_correct_type(self):
        self.assertIsInstance(self.subcategory.id, str)

    def test_id_field_has_correct(self):
        self.assertEqual(self.subcategory.id, self.id)

    def test_object_name_is_correct(self):
        object_name = f"Subcategory: id={self.id}"
        self.assertEqual(object_name, str(self.subcategory))


class UOMModelTest(TestCase):
    """Класс тестов модели UOM."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.title = "А" * 150
        cls.id = random.randint(1, 100)
        cls.uom = UOM.objects.create(id=cls.id, title=cls.title)

    def test_id_field_has_correct_type(self):
        self.assertIsInstance(self.uom.id, int)

    def test_id_field_has_correct(self):
        self.assertEqual(self.uom.id, self.id)

    def test_object_name_is_correct(self):
        object_name = f"UOM: id={self.id}, title={self.title}"
        self.assertEqual(object_name, str(self.uom))


class StockKeepingUnitTest(TestCase):
    """Класс тестов модели StockKeepingUnit."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.id = secrets.token_hex(16)
        cls.group: Group = GroupFactory()
        cls.category: Category = CategoryFactory()
        cls.subcategory: Subcategory = SubCategoryFactory()
        cls.uom: UOM = UOMFactory()
        cls.sku: StockKeepingUnit = StockKeepingUnit.objects.create(
            id=cls.id,
            group_id=cls.group,
            cat_id=cls.category,
            subcat_id=cls.subcategory,
            uom_id=cls.uom,
        )

    def test_object_was_created(self):
        self.assertEquals(StockKeepingUnit.objects.count(), 1)

    def test_id_field_has_correct_type(self):
        self.assertIsInstance(self.sku.id, str)

    def test_id_field_has_correct(self):
        self.assertEqual(self.sku.id, self.id)

    def test_object_name_is_correct(self):
        object_name = f"Product: id={self.id}"
        self.assertEqual(object_name, str(self.sku))

    def test_relations_work_correctly(self):
        for model in (self.group, self.category, self.subcategory, self.uom):
            with self.subTest(model=model):
                self.assertEqual(model.products.count(), 1)
                self.assertEqual(model.products.first(), self.sku)

    def test_deleting_work_correctly(self):
        for model in (self.group, self.category, self.subcategory, self.uom):
            with self.subTest(model=model):
                self.assertRaises(RestrictedError, model.delete)

    def test_correctly_verbose_name(self):
        field_verbose_name = {
            "title": "Наименование",
            "group_id": "Группа товара",
            "cat_id": "Категория товара",
            "subcat_id": "Подкатегория товара",
            "uom_id": "Вес/шт",
        }
        for fields, verbose_name in field_verbose_name.items():
            with self.subTest(fields=fields):
                self.assertEquals(
                    self.sku._meta.get_field(fields).verbose_name,
                    verbose_name,
                )
