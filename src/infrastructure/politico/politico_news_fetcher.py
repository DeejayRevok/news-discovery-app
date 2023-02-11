from typing import Iterable

from requests import HTTPError, get

from domain.new.new import New
from domain.new.news_fetch_exception import NewsFetchException
from domain.new.news_fetcher import NewsFetcher
from domain.new.news_source import NewsSource
from infrastructure.politico.politico_response_to_news_transformer import PoliticoResponseToNewsTransformer


class PoliticoNewsFetcher(NewsFetcher):
    __POLITICO_RSS_ADDRESS = "https://www.politico.com/rss/politicopicks.xml"

    def __init__(self, response_to_news_transformer: PoliticoResponseToNewsTransformer):
        self.__response_to_news_transformer = response_to_news_transformer

    def fetch(self) -> Iterable[New]:
        response = get(self.__POLITICO_RSS_ADDRESS)

        try:
            response.raise_for_status()
        except HTTPError as httperr:
            raise NewsFetchException(NewsSource.POLITICO, str(httperr))

        yield from self.__response_to_news_transformer.transform(response)
