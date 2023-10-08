from django.contrib import admin

from .models import Forecast, ForecastData


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Forecast."""

    list_display = ("id", "store", "sku", "forecast_date")


@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели ForecastData."""

    list_display = ("id", "forecast_id", "data")
