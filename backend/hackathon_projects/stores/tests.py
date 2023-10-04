import secrets

from django.db.models.deletion import RestrictedError
from django.test import TestCase

from core.model_factories.store_factory import (
    CityFactory,
    DivisionFactory,
    FormatFactory,
    LocationFactory,
    SizeFactory,
)
from .models import City, Division, Format, Location, Size, Store


class CityModelTests(TestCase):
    """Класс тестов модели City."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.id: str = secrets.token_hex(16)
        cls.city: City = City.objects.create(id=cls.id)

    def test_object_was_created(self):
        self.assertEquals(City.objects.count(), 1)

    def test_fields_has_correct_type(self):
        self.assertIsInstance(self.city.id, str)
        self.assertIsInstance(self.city.title, str)

    def test_city_object_name_is_correct(self):
        expected_object_name = f"City: id={self.id}"
        self.assertEqual(expected_object_name, str(self.city))

    def test_title_field_has_correct_verbose_name(self):
        self.assertEquals(
            self.city._meta.get_field("title").verbose_name,
            "Название города",
        )


class DivisionModelTests(TestCase):
    """Класс тестов модели Division."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.id: str = secrets.token_hex(16)
        cls.division: Division = Division.objects.create(id=cls.id)

    def test_object_was_created(self):
        self.assertEquals(Division.objects.count(), 1)

    def test_fields_has_correct_type(self):
        self.assertIsInstance(self.division.id, str)
        self.assertIsInstance(self.division.title, str)

    def test_division_object_name_is_correct(self):
        expected_object_name = f"Division: id={self.id}"
        self.assertEqual(expected_object_name, str(self.division))

    def test_title_field_has_correct_verbose_name(self):
        self.assertEquals(
            self.division._meta.get_field("title").verbose_name,
            "Название подразделения",
        )


class FormatModelTests(TestCase):
    """Класс тестов модели Format."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.title: str = "Random Type 1"
        cls.format: Format = Format.objects.create(title=cls.title)

    def test_object_was_created(self):
        self.assertEquals(Format.objects.count(), 1)

    def test_fields_has_correct_types(self):
        self.assertIsInstance(self.format.id, int)
        self.assertIsInstance(self.format.title, str)

    def test_title_field_has_correct_verbose_name(self):
        self.assertEquals(
            self.format._meta.get_field("title").verbose_name,
            "Формат супермаркета",
        )

    def test_format_object_name_is_correct(self):
        expected_object_name = (
            f"Format: id={self.format.id}, title={self.title}"
        )
        self.assertEqual(expected_object_name, str(self.format))


class LocationModelTests(TestCase):
    """Класс тестов модели Location."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.type: str = "Random Type 123"
        cls.location: Location = Location.objects.create(type=cls.type)

    def test_object_was_created(self):
        self.assertEquals(Location.objects.count(), 1)

    def test_fields_has_correct_types(self):
        self.assertIsInstance(self.location.id, int)
        self.assertIsInstance(self.location.type, str)

    def test_type_field_has_correct_verbose_name(self):
        self.assertEquals(
            self.location._meta.get_field("type").verbose_name,
            "Тип локации/окружения",
        )

    def test_format_object_name_is_correct(self):
        expected_object_name = (
            f"Location: id={self.location.id}, type={self.type}"
        )
        self.assertEqual(expected_object_name, str(self.location))


class SizeModelTests(TestCase):
    """Класс тестов модели Size."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.type: str = "Random Type 123"
        cls.size: Size = Size.objects.create(type=cls.type)

    def test_object_was_created(self):
        self.assertEquals(Size.objects.count(), 1)

    def test_fields_has_correct_types(self):
        self.assertIsInstance(self.size.id, int)
        self.assertIsInstance(self.size.type, str)

    def test_type_field_has_correct_verbose_name(self):
        self.assertEquals(
            self.size._meta.get_field("type").verbose_name,
            "Тип размера",
        )

    def test_size_object_name_is_correct(self):
        expected_object_name = f"Size: id={self.size.id}, type={self.type}"
        self.assertEqual(expected_object_name, str(self.size))


class StoreModelTests(TestCase):
    """Класс тестов модели Store."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.store_id: str = secrets.token_hex(16)
        cls.city: City = CityFactory()
        cls.division: Division = DivisionFactory()
        cls.format: Format = FormatFactory()
        cls.location: Location = LocationFactory()
        cls.size: Size = SizeFactory()
        cls.store: Store = Store.objects.create(
            id=cls.store_id,
            city=cls.city,
            division=cls.division,
            type_format=cls.format,
            loc=cls.location,
            size=cls.size,
            is_active=True,
        )

    def test_object_was_created(self):
        self.assertEquals(Store.objects.count(), 1)

    def test_fields_has_correct_types(self):
        self.assertIsInstance(self.store.id, str)
        self.assertIsInstance(self.store.title, str)
        self.assertIsInstance(self.store.city, City)
        self.assertIsInstance(self.store.division, Division)
        self.assertIsInstance(self.store.type_format, Format)
        self.assertIsInstance(self.store.loc, Location)
        self.assertIsInstance(self.store.size, Size)
        self.assertIsInstance(self.store.is_active, bool)

    def test_relations_work_correctly(self):
        for model in (
            self.city,
            self.division,
            self.format,
            self.location,
            self.size,
        ):
            with self.subTest(model=model):
                self.assertEquals(model.stores.count(), 1)
                self.assertEquals(model.stores.first(), self.store)

    def test_store_fields_has_correct_verbose_names(self):
        field_verbose_name: dict = {
            "title": "Название супермаркета",
            "city": "Город",
            "division": "Подразделение",
            "type_format": "Формат магазина",
            "loc": "Местоположение",
            "size": "Размер",
            "is_active": "Флаг активного магазина",
        }
        for field, verbose_name in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEquals(
                    self.store._meta.get_field(field).verbose_name,
                    verbose_name,
                )

    def test_store_object_name_is_correct(self):
        expected_object_name = f"Store: id={self.store_id}"
        self.assertEqual(expected_object_name, str(self.store))

    def test_deleting_related_models_raises_exception(self):
        for model in (
            self.city,
            self.division,
            self.format,
            self.location,
            self.size,
        ):
            with self.subTest(model=model):
                self.assertRaises(RestrictedError, model.delete)
