from domain.new.news_fetcher import NewsFetcher
from domain.new.news_fetcher_not_implemented_exception import NewsFetcherNotImplementedException
from domain.new.news_fetcher_selector import NewsFetcherSelector
from domain.new.news_source import NewsSource
from infrastructure.abc.abc_news_fetcher import ABCNewsFetcher
from infrastructure.confidencial.confidencial_news_fetcher import ConfidencialNewsFetcher
from infrastructure.politico.politico_news_fetcher import PoliticoNewsFetcher


class ThirdPartyNewsFetcherSelector(NewsFetcherSelector):
    def __init__(
        self,
        abc_fetcher: ABCNewsFetcher,
        confidencial_fetcher: ConfidencialNewsFetcher,
        politico_fetcher: PoliticoNewsFetcher,
    ):
        self.__abc_fetcher = abc_fetcher
        self.__confidencial_fetcher = confidencial_fetcher
        self.__politico_fetcher = politico_fetcher

    def select(self, news_source: NewsSource) -> NewsFetcher:
        if news_source == NewsSource.ABC:
            return self.__abc_fetcher
        if news_source == NewsSource.CONFIDENCIAL:
            return self.__confidencial_fetcher
        if news_source == NewsSource.POLITICO:
            return self.__politico_fetcher
        raise NewsFetcherNotImplementedException(news_source)
