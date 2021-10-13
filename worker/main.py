import sys

from celery.concurrency import asynpool
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking
from news_service_lib.server_utils import server_args_parser

from news_service_lib.log_utils import add_logstash_handler

from news_service_lib.config_utils import load_config

from news_service_lib.base_celery_app import BaseCeleryApp

from config import config
from log_config import LOG_CONFIG, get_logger
from worker.container_config import load, container

asynpool.PROC_ALIVE_TIMEOUT = 60.0
CELERY_APP = BaseCeleryApp("News discovery app", ["worker.celery_tasks"])
LOGGER = get_logger()


def main(config_path: str):
    load_config(config_path, config, "NEWS_DISCOVERY")
    load()
    publisher = container.get("exchange_publisher")
    if not publisher.test_connection():
        LOGGER.error("Error connecting to the queue provider. Exiting...")
        sys.exit(1)

    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    CELERY_APP.configure(
        task_queue_name="news-discovery", broker_config=config.rabbit, worker_concurrency=config.celery.concurrency
    )

    apm_client = Client(
        config={
            "SERVICE_NAME": "news-discovery-app",
            "SECRET_TOKEN": config.elastic_apm.secret_token,
            "SERVER_URL": config.elastic_apm.url,
        }
    )
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_APP.run()


if __name__ == "__main__":
    args = server_args_parser("News discovery application")
    main(args["configuration"])
