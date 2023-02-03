from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.discover_news.discover_news_command_handler.DiscoverNewsCommandHandler",
            "application.discover_news.discover_news_command_handler.DiscoverNewsCommandHandler",
            [
                Argument.no_kw_argument("@infrastructure.third_party_news_fetcher_selector.ThirdPartyNewsFetcherSelector"),
                Argument.no_kw_argument("@bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus"),
                Argument.no_kw_argument("@logging.Logger"),
            ]
        )
    )
