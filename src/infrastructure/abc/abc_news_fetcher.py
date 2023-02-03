from typing import Iterable

from fake_useragent import UserAgent
from requests import get, HTTPError

from domain.new.new import New
from domain.new.news_fetch_exception import NewsFetchException
from domain.new.news_fetcher import NewsFetcher
from domain.new.news_source import NewsSource
from infrastructure.abc.abc_response_to_news_transformer import ABCResponseToNewsTransformer


class ABCNewsFetcher(NewsFetcher):
    __ABC_SAN_FRANCISCO_RSS_ADDRESS = "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml"

    def __init__(self, response_to_news_transformer: ABCResponseToNewsTransformer):
        self.__response_to_news_transformer = response_to_news_transformer

    def fetch(self) -> Iterable[New]:
        user_agent = UserAgent()
        response = get(self.__ABC_SAN_FRANCISCO_RSS_ADDRESS, headers={
            "User-Agent": user_agent.random
        })

        try:
            response.raise_for_status()
        except HTTPError as httperr:
            raise NewsFetchException(NewsSource.ABC, str(httperr))

        yield from self.__response_to_news_transformer.transform(response)
