from abc import abstractmethod

from domain.new.news_fetcher import NewsFetcher
from domain.new.news_source import NewsSource


class NewsFetcherSelector:
    @abstractmethod
    def select(self, news_source: NewsSource) -> NewsFetcher:
        pass
