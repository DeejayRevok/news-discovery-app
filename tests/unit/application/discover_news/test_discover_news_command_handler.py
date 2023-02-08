from logging import Logger
from unittest import TestCase
from unittest.mock import Mock, call

from domain.new.new_discovered_event import NewDiscoveredEvent

from application.discover_news.discover_news_command import DiscoverNewsCommand
from bus_station.event_terminal.bus.event_bus import EventBus
from domain.new.news_fetcher import NewsFetcher

from domain.new.language import Language

from domain.new.news_source import NewsSource

from domain.new.new import New

from domain.new.news_fetcher_selector import NewsFetcherSelector

from application.discover_news.discover_news_command_handler import DiscoverNewsCommandHandler


class TestDiscoverNewsCommandHandler(TestCase):
    def setUp(self) -> None:
        self.news_fetcher_selector_mock = Mock(spec=NewsFetcherSelector)
        self.event_bus_mock = Mock(spec=EventBus)
        self.logger_mock = Mock(spec=Logger)
        self.command_handler = DiscoverNewsCommandHandler(
            self.news_fetcher_selector_mock, self.event_bus_mock, self.logger_mock
        )

    def test_handle_success(self):
        test_new = New(
            title="test_new",
            url="test_url",
            content="test_content",
            source=NewsSource.ABC,
            date=1231312.89,
            language=Language.ENGLISH,
            image="test_image",
        )
        test_news_fetcher = Mock(spec=NewsFetcher)
        self.news_fetcher_selector_mock.select.return_value = test_news_fetcher
        test_news_fetcher.fetch.return_value = [test_new, test_new]
        test_command = DiscoverNewsCommand(news_source="ABC")

        self.command_handler.handle(test_command)

        self.news_fetcher_selector_mock.select.assert_called_once_with(NewsSource.ABC)
        test_news_fetcher.fetch.assert_called_once_with()
        self.event_bus_mock.transport.assert_has_calls(
            [
                call(
                    NewDiscoveredEvent(
                        title="test_new",
                        content="test_content",
                        url="test_url",
                        date=1231312.89,
                        language=Language.ENGLISH.value,
                        source=NewsSource.ABC.value,
                        image="test_image",
                    )
                ),
                call(
                    NewDiscoveredEvent(
                        title="test_new",
                        content="test_content",
                        url="test_url",
                        date=1231312.89,
                        language=Language.ENGLISH.value,
                        source=NewsSource.ABC.value,
                        image="test_image",
                    )
                ),
            ]
        )
