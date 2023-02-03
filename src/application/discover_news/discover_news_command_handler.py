from logging import Logger

from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.event_terminal.bus.event_bus import EventBus

from domain.new.new import New
from application.discover_news.discover_news_command import DiscoverNewsCommand
from domain.new.new_discovered_event import NewDiscoveredEvent
from domain.new.news_fetcher_selector import NewsFetcherSelector
from domain.new.news_source import NewsSource


class DiscoverNewsCommandHandler(CommandHandler):
    def __init__(self, news_fetcher_selector: NewsFetcherSelector, event_bus: EventBus, logger: Logger):
        self.__news_fetcher_selector = news_fetcher_selector
        self.__event_bus = event_bus
        self.__logger = logger

    def handle(self, command: DiscoverNewsCommand) -> None:
        self.__logger.info(f"Starting discovering news from {command.news_source}")
        news_source = NewsSource(command.news_source)
        news_fetcher = self.__news_fetcher_selector.select(news_source)
        for new in news_fetcher.fetch():
            self.__logger.info(f"Discovered new with title {new.title}")
            self.__event_bus.transport(
                self.__create_event_from_new(new)
            )
        self.__logger.info(f"Finished discovering news from {command.news_source}")

    def __create_event_from_new(self, new: New) -> NewDiscoveredEvent:
        return NewDiscoveredEvent(
            title=new.title,
            url=new.url,
            content=new.content,
            source=new.source.value,
            date=new.date,
            language=new.language.value,
            image=new.image
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.news_discovery.discover_news"
