from django.db import models
from django.db.models import JSONField

from products.models import StockKeepingUnit
from stores.models import Store


class Forecast(models.Model):
    """Модель прогноза спроса."""

    store = models.ForeignKey(
        Store,
        on_delete=models.RESTRICT,
        verbose_name='Супермаркет',
        related_name='forecasts',
        help_text='Супермаркет',
    )
    sku = models.ForeignKey(
        StockKeepingUnit,
        on_delete=models.RESTRICT,
        verbose_name='Товар',
        related_name='forecasts',
        help_text='Товар',
    )
    forecast_date = models.DateField(
        verbose_name='Дата',
        help_text='Дата',
    )

    class Meta:
        verbose_name = "Прогноз"
        verbose_name_plural = "Прогнозы"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"Forecast_id: {self.id}"


class ForecastData(models.Model):
    """Модель данных прогноза."""

    forecast_id = models.ForeignKey(
        Forecast,
        on_delete=models.RESTRICT,
        verbose_name='ID прогноза',
        help_text='ID прогноза',
    )
    data = JSONField(default=dict)

    class Meta:
        db_table = 'forecastdata'
        verbose_name = "Данные прогноза"
        verbose_name_plural = "Данные прогнозов"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"ForecastData: forecast_id={self.forecast_id}"
