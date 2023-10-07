import requests
from django.conf import settings
from loguru import logger
from rest_framework import status


def send_signal_to_ds_service():
    """Уведомляет DS сервис о готовности данных для прогноза."""
    try:
        response = requests.get(settings.DS_START_FORECAST_URL)
        if response.status_code == status.HTTP_200_OK:
            logger.info(
                "DS сервис успешно получил сигнал о готовности данных."
            )
        else:
            logger.error("DS сервис недоступен.")
    except requests.exceptions.ConnectionError as er:
        logger.error(er)
