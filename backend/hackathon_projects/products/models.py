from django.db import models

from .constants import FORMAT_TITLE_MAX_LEN, HASHED_ID_MAX_LEN


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


class StockKeepingUnit(BaseIDModel):
    """Модель товара."""

    title = models.CharField(
        max_length=FORMAT_TITLE_MAX_LEN,
        null=True,
        verbose_name="Наименование",
        help_text="Наименование",
    )
    group_id = models.ForeignKey(
        'Group',
        on_delete=models.RESTRICT,
        verbose_name="Группа товара",
        related_name="products",
        help_text="ID группы товара",
    )
    cat_id = models.ForeignKey(
        'Category',
        on_delete=models.RESTRICT,
        verbose_name="Категория товара",
        related_name="products",
        help_text="ID категории товара",
    )
    subcat_id = models.ForeignKey(
        'Subcategory',
        on_delete=models.RESTRICT,
        verbose_name="Подкатегория товара",
        related_name="products",
        help_text="ID подкатегории товара",
    )
    uom_id = models.ForeignKey(
        'UOM',
        on_delete=models.RESTRICT,
        verbose_name="Вес/шт",
        related_name="products",
        help_text="ID маркера товара (вес/шт)",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Product: id={self.id}"


class Group(BaseIDModel):
    """Модель группы товара."""

    class Meta:
        verbose_name = "Группа товара"
        verbose_name_plural = "Группы товаров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Group: id={self.id}"


class Category(BaseIDModel):
    """Модель категории товара."""

    group_id = models.ForeignKey(
        Group,
        on_delete=models.RESTRICT,
        verbose_name="Группа категории товара",
        related_name="category",
        help_text="ID группы категории товара",
    )

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Category: id={self.id}"


class Subcategory(BaseIDModel):
    """Модель подкатегории товара."""

    category_id = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        verbose_name="Категория товара",
        related_name="subcategory",
        help_text="ID категории товара",
    )

    class Meta:
        verbose_name = "Подкатегория товара"
        verbose_name_plural = "Подкатегории товаров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Subcategory: id={self.id}"


class UOM(models.Model):
    """Модель маркера товара,
    обозначающего продается товар на вес или в шт.
    """
    id = models.IntegerField(
        primary_key=True,
        db_index=True,
        verbose_name="ID",
        help_text="ID",
    )
    title = models.CharField(
        max_length=FORMAT_TITLE_MAX_LEN,
        blank=True,
        verbose_name="Наименование",
        help_text="Наименование",
    )

    class Meta:
        verbose_name = "Маркер товара"
        verbose_name_plural = "Маркеры товаров"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"UOM: id={self.id}, title={self.title}"
