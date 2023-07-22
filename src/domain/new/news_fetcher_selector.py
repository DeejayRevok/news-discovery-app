from abc import abstractmethod, ABC

from domain.new.news_fetcher import NewsFetcher
from domain.new.news_source import NewsSource


class NewsFetcherSelector(ABC):
    @abstractmethod
    def select(self, news_source: NewsSource) -> NewsFetcher:
        pass
