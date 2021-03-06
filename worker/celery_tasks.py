from dataclasses import asdict

from celery.signals import worker_process_init, worker_process_shutdown

from news_service_lib.messaging.exchange_publisher import ExchangePublisher

from config import config
from log_config import get_logger
from worker.container_config import container
from worker.main import CELERY_APP
from discovery.definitions import DEFINITIONS

LOGGER = get_logger()


@worker_process_init.connect()
def initialize_worker(*_, **__):
    LOGGER.info("Initializing worker")
    exchange_publisher: ExchangePublisher = container.get("exchange_publisher")
    exchange_publisher.connect()
    exchange_publisher.initialize()


@CELERY_APP.app.task(name="discover_news")
def discover_news(definition_name: str):
    if "rabbit" in config:
        LOGGER.info(f"Executing discovery {definition_name}")
        definition = DEFINITIONS[definition_name]
        definition_instance = definition["class"](definition)

        exchange_publisher: ExchangePublisher = container.get("exchange_publisher")

        for discovered_new in definition_instance():
            exchange_publisher(asdict(discovered_new))

    else:
        LOGGER.error("Worker configuration not initialized")


@worker_process_shutdown.connect()
def shutdown_worker(*_, **__):
    LOGGER.info("Shutting down worker")
    exchange_publisher: ExchangePublisher = container.get("exchange_publisher")
    exchange_publisher.shutdown()
