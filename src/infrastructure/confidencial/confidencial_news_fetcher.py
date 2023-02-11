from typing import Iterable

from requests import HTTPError, get

from domain.new.new import New
from domain.new.news_fetch_exception import NewsFetchException
from domain.new.news_fetcher import NewsFetcher
from domain.new.news_source import NewsSource
from infrastructure.confidencial.confidencial_response_to_news_transformer import ConfidencialResponseToNewsTransformer


class ConfidencialNewsFetcher(NewsFetcher):
    __CONFIDENCIAL_RSS_ADDRESS = "https://rss.elconfidencial.com/mundo/"

    def __init__(self, response_to_news_transformer: ConfidencialResponseToNewsTransformer):
        self.__response_to_news_transformer = response_to_news_transformer

    def fetch(self) -> Iterable[New]:
        response = get(self.__CONFIDENCIAL_RSS_ADDRESS)

        try:
            response.raise_for_status()
        except HTTPError as httperr:
            raise NewsFetchException(NewsSource.CONFIDENCIAL, str(httperr))

        yield from self.__response_to_news_transformer.transform(response)
