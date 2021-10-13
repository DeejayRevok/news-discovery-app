from unittest import TestCase
from unittest.mock import MagicMock

from discovery.fetch_implementations.fetch_rss_news_implementation import FetchRssNewsImplementation


class TestFetchRSSImplementation(TestCase):
    def test_fetch(self):
        source_adapter_1 = MagicMock()
        source_adapter_2 = MagicMock()
        test_definition = dict(source_adapters=[source_adapter_1, source_adapter_2])
        list(FetchRssNewsImplementation(test_definition)())
        source_adapter_1().fetch.assert_called_once()
        source_adapter_2().fetch.assert_called_once()
