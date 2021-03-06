from celery.schedules import crontab
from elasticapm import Client
from elasticapm.contrib.celery import register_instrumentation, register_exception_tracking
from news_service_lib.log_utils import add_logstash_handler
from news_service_lib.server_utils import server_args_parser
from news_service_lib.base_celery_app import BaseCeleryApp
from news_service_lib.config_utils import load_config

from config import config
from log_config import LOG_CONFIG, get_logger
from discovery.definitions import DEFINITIONS
from worker.celery_tasks import discover_news

CELERY_BEAT = BaseCeleryApp("News discovery app beat")
LOGGER = get_logger()


@CELERY_BEAT.app.on_after_configure.connect
def setup_periodic_tasks(sender, **__):
    LOGGER.info("Configuring news discovery beat")
    for definition_key, definition_value in DEFINITIONS.items():
        cron_definition = definition_value["cron_expression"].split(" ")
        sender.add_periodic_task(crontab(*cron_definition), discover_news.s(definition_key), name=definition_key)


def main(config_path: str):
    load_config(config_path, config, "NEWS_DISCOVERY")

    add_logstash_handler(LOG_CONFIG, config.logstash.host, config.logstash.port)
    CELERY_BEAT.configure(task_queue_name="news-discovery", broker_config=config.rabbit)

    apm_client = Client(
        config={
            "SERVICE_NAME": "news-discovery-beat",
            "SECRET_TOKEN": config.elastic_apm.secret_token,
            "SERVER_URL": config.elastic_apm.url,
        }
    )
    register_instrumentation(apm_client)
    register_exception_tracking(apm_client)

    CELERY_BEAT.run(beat=True)


if __name__ == "__main__":
    args = server_args_parser("News discovery beat application")
    main(args["configuration"])
