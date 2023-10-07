import argparse
import json
import logging
import os

import requests
import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import forecast

app = FastAPI()
ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
dataDir = "tmp/"

CREDENTIALS = {
    "email": os.getenv("DS_SERVICE_LOGIN", default="ds@mail.ru"),
    "password": os.getenv("DS_SERVICE_PASSWORD", default="ds_password"),
}

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.DEBUG)
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s"
)
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)


def send_signal_to_back():
    """Logs in and sends signal to backend."""
    try:
        login_resp = requests.post(
            "http://localhost/auth/token/login/", data=CREDENTIALS
        )
        token = login_resp.json().get("auth_token")
        if not token:
            app_logger.info("Authorization FAILED.")
            return
        app_logger.info("Authorization succeeded.")

        headers = {"Authorization": f"Token {token}"}
        signal_resp = requests.get(
            "http://localhost/api/v1/import-forecasts/", headers=headers
        )
        if signal_resp.status_code == 200:
            app_logger.info("Backend was notified.")
            return
        app_logger.info("Backend was not notified.")

    except (requests.exceptions.ConnectionError, Exception) as er:
        app_logger.info("Backend is not available.")


def make_forecast(path: str) -> None:
    """Runs forecast and saves result."""
    app_logger.info(f"data successfully loaded")
    result, status, problem_pairs = forecast(path)
    message = "forecast successfully finished, results saved"
    if status != "OK":
        app_logger.error(f"forecast failed")
        message = "forecast failed"
    else:
        app_logger.info(f"forecast finished")
        with open(dataDir + "forecast_archive.json", "w") as file:
            json.dump(result, file)
            app_logger.info(f"data saved")
    app_logger.info(message)
    # resp = requests.get("http://localhost:8001/ds/ready")  # for local tests
    send_signal_to_back()


# for local tests
# @app.get("/ds/ready")
# def forecast_ready():
#     pass


@app.get("/ds/start")
async def main(background_tasks: BackgroundTasks) -> dict:
    """Runs forecast in the background."""
    background_tasks.add_task(make_forecast, path=dataDir + "ds_data.csv")
    return {"message": "forecast is running. wait please"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=7000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)
