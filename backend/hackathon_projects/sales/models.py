from django.core.validators import MinValueValidator
from django.db import models

from products.models import StockKeepingUnit
from stores.models import Store
from .constants import DECIMAL_MAX_DIGITS, DECIMAL_MIN_VAL, DECIMAL_PLACES_VAL


class Sale(models.Model):
    """Модель продажи товара в супермаркете."""

    store_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="sales",
        verbose_name="Супермаркет",
    )
    sku_id = models.ForeignKey(
        StockKeepingUnit,
        on_delete=models.CASCADE,
        related_name="sales",
        verbose_name="Товар",
    )

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ("id",)

    def __str__(self) -> str:
        return (
            f"Sale: id={self.id}, store_id={self.store_id}, "
            f"sku_id={self.sku_id}"
        )


class SaleInfo(models.Model):
    """Модель информации о продаже."""

    sale_id = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="sale_info",
        verbose_name="Продажа",
    )
    date = models.DateField(verbose_name="Дата продажи")
    sales_type = models.BooleanField(verbose_name="Флаг наличия промо")
    sales_units = models.DecimalField(
        verbose_name="Число проданных товаров без признака промо",
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES_VAL,
        validators=[MinValueValidator(DECIMAL_MIN_VAL)],
    )
    sales_units_promo = models.DecimalField(
        verbose_name="Число проданных товаров с признаком промо",
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES_VAL,
        validators=[MinValueValidator(DECIMAL_MIN_VAL)],
    )
    sales_rub = models.DecimalField(
        verbose_name="Продажи без признака промо в рублях",
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES_VAL,
        validators=[MinValueValidator(DECIMAL_MIN_VAL)],
    )
    sales_rub_promo = models.DecimalField(
        verbose_name="Продажи с признаком промо в рублях",
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES_VAL,
        validators=[MinValueValidator(DECIMAL_MIN_VAL)],
    )

    class Meta:
        verbose_name = "Информация о продаже"
        verbose_name_plural = "Информация о продажах"
        ordering = ("date",)

    def __str__(self) -> str:
        return (
            f"SaleInfo: id={self.id}, sale_id={self.sale_id}, date={self.date}"
        )
