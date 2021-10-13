from news_service_lib.configurable_container import ConfigurableContainer

from news_service_lib.messaging.exchange_publisher import ExchangePublisher

from config import config
from log_config import get_logger

container: ConfigurableContainer = ConfigurableContainer([], config)


def load():
    container.set(
        "exchange_publisher", ExchangePublisher(**config.rabbit, exchange="news-internal-exchange", logger=get_logger())
    )
