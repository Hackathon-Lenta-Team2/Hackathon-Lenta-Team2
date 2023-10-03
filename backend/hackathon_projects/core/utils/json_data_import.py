import json
import os

from django.conf import settings
from django.db import transaction

from forecasts.models import Forecast, ForecastData


def import_data_from_json(json_obj):
    """Функция импорта данных из JSON в БД."""

    try:
        if isinstance(json_obj, str):
            file_path = os.path.join(settings.DATA_FILES_DIR, json_obj)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
    except json.JSONDecodeError as e:
        raise ValueError("Ошибка в формате JSON: {}".format(str(e)))
    forecasts_to_insert = []
    forecast_data_to_insert = []

    with transaction.atomic():
        for item in data['data']:
            try:
                store_id = item['store']
                sku_id = item['forecast']['sku']
                forecast_date = item['forecast_date']
                forecast_data = item['forecast']['sales_units']
            except KeyError as e:
                raise ValueError(
                    "Отсутствует обязательное поле в JSON: {}".format(str(e)))

            forecast = Forecast(
                store_id=store_id,
                sku_id=sku_id,
                forecast_date=forecast_date
            )
            forecasts_to_insert.append(forecast)

            forecast_data_object = ForecastData(
                forecast_id=forecast,
                data=forecast_data
            )
            forecast_data_to_insert.append(forecast_data_object)

        Forecast.objects.bulk_create(forecasts_to_insert)

        forecast_id_mapping = {
            forecast: forecast.id for forecast in forecasts_to_insert}

        for forecast_data_object in forecast_data_to_insert:
            forecast_data_object.forecast_id_id = forecast_id_mapping[
                forecast_data_object.forecast_id]

        ForecastData.objects.bulk_create(forecast_data_to_insert)
