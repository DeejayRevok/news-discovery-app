"""
ABC rss news adapter module
"""
from news_service_lib.models.language import Language
from time import mktime, strptime
from typing import Iterator
from xml.etree.ElementTree import fromstring, tostring, Element

import requests
from bs4 import BeautifulSoup
from lxml import html
from xmltodict import parse
from news_service_lib.models.new import New

from discovery.adapters.source_adapter import SourceAdapter
from log_config import get_logger


LOGGER = get_logger()


class ABCRssNewsAdapter(SourceAdapter):
    DATE_INPUT_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
    ROOT_NEW_TAG = "item"

    def _fetch(self) -> Iterator[Element]:
        LOGGER.info("Fetching news from %s", self.source_params["abc_rss"])
        response = requests.get(self.source_params["abc_rss"])
        rss = fromstring(response.content)
        for channel in rss:
            for item in channel:
                if item.tag == self.ROOT_NEW_TAG:
                    yield item

    def _adapt_single(self, item: Element) -> New:
        new_dict = parse(tostring(item).decode(), attr_prefix="")[self.ROOT_NEW_TAG]
        LOGGER.info("Found new with title %s", new_dict["title"])

        content = self.__parse_content(new_dict["description"])

        date = mktime(strptime(new_dict["pubDate"], self.DATE_INPUT_FORMAT))

        return New(
            title=new_dict["title"],
            url=new_dict["link"],
            content=content,
            source="ABC",
            date=date,
            language=Language.SPANISH.value,
        )

    def __parse_content(self, html_string: str) -> str:
        if html.fromstring(html_string).find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self.__parse_content(html_content)
        else:
            return html_string
