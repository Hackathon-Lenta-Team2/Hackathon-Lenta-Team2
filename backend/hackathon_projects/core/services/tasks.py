import time

from core.services.celery_app import app


@app.task()
def debug_task(string: str):
    time.sleep(10)
    print(f"Hello from debug_task. {string=}")
    print(f"Hello from debug_task. {string=}")
    print(f"Hello from debug_task. {string=}")
    print(f"Hello from debug_task. {string=}")

    # вызывать так debug_task.delay("Бла бла")
