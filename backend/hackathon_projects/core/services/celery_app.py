import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackathon_projects.settings")

app = Celery("hackathon_projects")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every day at an hour specified in .env.
    # Env var - RUN_DS_DATA_PREPARATION_CRON_HOUR.
    "prepare_ds_data_every_day": {
        "task": "tasks.collect_sales_data_for_ds_service",
        "schedule": crontab(hour=settings.RUN_DS_DATA_PREPARATION_CRON_HOUR),
    },
}
