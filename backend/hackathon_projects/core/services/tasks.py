from celery import shared_task
from loguru import logger

from core.utils.csv_writer import CSVWriter
from core.utils.json_data_import import import_data_from_json
from core.utils.requests import send_signal_to_ds_service


@shared_task(name="tasks.ds_data_import_task")
def ds_data_import_task() -> None:
    """Запускает импорт данных от DS сервиса в БД с помощью Celery."""
    try:
        import_data_from_json("forecast_archive.json")
        logger.info("Импорт завершён.")
    except Exception as err:
        error_message = f"Unexpected {err=}"
        logger.error(error_message)


@shared_task(name="tasks.collect_sales_data_for_ds_service")
def collect_sales_data_for_ds_service() -> None:
    """Собирает данные фактических продаж.
    Пишет данные в ds_data.csv и уведомляет ds сервис.
    """
    # записать файл данных
    CSVWriter().write()
    # послать сигнал ds сервису
    send_signal_to_ds_service()
