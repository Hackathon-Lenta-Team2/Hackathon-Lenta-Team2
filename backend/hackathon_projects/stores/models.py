from django.db import models

from .constants import (
    CITY_TITLE_MAX_LEN,
    DIVISION_TITLE_MAX_LEN,
    FORMAT_TITLE_MAX_LEN,
    HASHED_ID_MAX_LEN,
    LOC_TYPE_MAX_LEN,
    SIZE_TYPE_MAX_LEN,
    STORE_TITLE_MAX_LEN,
)


class BaseIDModel(models.Model):
    """Абстрактная модель.
    Содержит поле id - хэш. ID фиксированной длины.
    """

    id = models.CharField(
        max_length=HASHED_ID_MAX_LEN,
        primary_key=True,
        db_index=True,
        verbose_name="ID",
        help_text="Хэшированный ID",
    )

    class Meta:
        abstract = True


class City(BaseIDModel):
    """Модель Города."""

    title = models.CharField(
        max_length=CITY_TITLE_MAX_LEN,
        verbose_name="Название города",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_default_city_title(self.id)
        super().save(*args, **kwargs)

    @staticmethod
    def get_default_city_title(id: str) -> str:
        return f"City {id}"

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"City: id={self.id}"


class Division(BaseIDModel):
    """Модель Подразделения."""

    title = models.CharField(
        max_length=DIVISION_TITLE_MAX_LEN,
        verbose_name="Название подразделения",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_default_division_title(self.id)
        super().save(*args, **kwargs)

    @staticmethod
    def get_default_division_title(id: str) -> str:
        return f"Division {id}"

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Division: id={self.id}"


class Format(models.Model):
    """Модель Формата супермаркетов."""

    title = models.CharField(
        max_length=FORMAT_TITLE_MAX_LEN, verbose_name="Формат супермаркета"
    )

    class Meta:
        verbose_name = "Формат супермаркетов"
        verbose_name_plural = "Форматы супермаркетов"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Format: id={self.id}, title={self.title}"


class Location(models.Model):
    """Модель типа локации/окружения супермаркета."""

    type = models.CharField(
        max_length=LOC_TYPE_MAX_LEN, verbose_name="Тип локации/окружения"
    )

    class Meta:
        verbose_name = "Тип локации/окружения"
        verbose_name_plural = "Типы локации/окружения"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Location: id={self.id}, type={self.type}"


class Size(models.Model):
    """Модель типа размера супермаркета."""

    type = models.CharField(
        max_length=SIZE_TYPE_MAX_LEN, verbose_name="Тип размера"
    )

    class Meta:
        verbose_name = "Размер супермаркетов"
        verbose_name_plural = "Размеры супермаркетов"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Size: id={self.id}, type={self.type}"


class Store(BaseIDModel):
    """Модель супермаркета."""

    title = models.CharField(
        max_length=STORE_TITLE_MAX_LEN,
        verbose_name="Название супермаркета",
        blank=True,
    )
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        verbose_name="Город",
        related_name="stores",
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.RESTRICT,
        verbose_name="Подразделение",
        related_name="stores",
    )
    type_format = models.ForeignKey(
        Format,
        on_delete=models.RESTRICT,
        verbose_name="Формат магазина",
        related_name="stores",
    )
    loc = models.ForeignKey(
        Location,
        on_delete=models.RESTRICT,
        verbose_name="Местоположение",
        related_name="stores",
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.RESTRICT,
        verbose_name="Размер",
        related_name="stores",
    )
    is_active = models.BooleanField(
        verbose_name="Флаг активного магазина", default=True
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_default_store_title(self.id)
        super().save(*args, **kwargs)

    @staticmethod
    def get_default_store_title(id: str) -> str:
        return f"Lenta {id}"

    class Meta:
        verbose_name = "Супермаркет"
        verbose_name_plural = "Супермаркеты"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Store: id={self.id}"
