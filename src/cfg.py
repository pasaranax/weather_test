import logging
import os
import time
from logging.config import dictConfig


class app:
    port = 8000
    debug = True
    owm_api_key = "f50c5388a13a8b50d29da3080602a60f"
    owm_url = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}"
    elastic_host = os.getenv("ELASTIC_HOST", "localhost")

    workdir = os.path.dirname(os.path.abspath(__file__))
    telegram_bot_token = None
    send_mail = "smtp"
    max_workers_on_executor = 4
    tornado_settings = {}
    sentry_url = ""
    sentry_client_kwargs = {}
    gzip_output = 0
    number_of_nodes = 1

    logging_config = {
        "version": 1,
        "formatters": {
            "basic": {
                "format": "%(asctime)s %(name)-16s %(levelname)-8s %(message)s"
            }
        },
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "formatter": "basic",
                "level": logging.DEBUG if debug else logging.INFO
            }
        },
        "root": {
            "handlers": ["stream"],
            "level": logging.DEBUG if debug else logging.INFO
        },
    }

    for handler in ["tornado", "peewee", "s3transfer", "googleapiclient.discovery"]:  # ignored logging users
        logging.getLogger(handler).setLevel(logging.ERROR)
    dictConfig(logging_config)
    os.environ["TZ"] = "UTC"
    time.tzset()
