from time import mktime, strptime
import requests
from xml.etree.ElementTree import Element, fromstring, tostring
from typing import ClassVar, Iterator, Optional

from bs4 import BeautifulSoup
from lxml import html
from xmltodict import parse
from news_service_lib.models.new import New
from news_service_lib.models.language import Language

from discovery.adapters.source_adapter import SourceAdapter
from log_config import get_logger

LOGGER = get_logger()


class PoliticoRSSNewsAdapter(SourceAdapter):
    __DATE_FORMAT: ClassVar[str] = "%a, %d %b %Y %H:%M:%S EST"
    __ROOT_NEW_TAG: ClassVar[str] = "item"

    def _fetch(self) -> Iterator[Element]:
        LOGGER.info("Fetching news from %s", self.source_params["politico_rss"])
        response = requests.get(self.source_params["politico_rss"])
        rss = fromstring(response.content)
        for channel in rss:
            for element in channel:
                if element.tag == self.__ROOT_NEW_TAG:
                    yield element

    def _adapt_single(self, item: Element) -> Optional[New]:
        raw_new_dict = parse(tostring(item).decode(), attr_prefix="")[self.__ROOT_NEW_TAG]
        LOGGER.info("Found new with title %s", raw_new_dict["title"])

        if "ns3:encoded" not in raw_new_dict:
            return None

        content = self.__parse_content(raw_new_dict["ns3:encoded"])
        date = mktime(strptime(raw_new_dict["pubDate"], self.__DATE_FORMAT))

        return New(
            title=raw_new_dict["title"],
            url=raw_new_dict["link"],
            content=content,
            source="Politico",
            date=date,
            language=Language.ENGLISH.value,
            image=self.__get_image_url(raw_new_dict),
        )

    def __parse_content(self, html_string: str) -> str:
        if html.fromstring(html_string).find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self.__parse_content(html_content)
        else:
            return html_string

    def __get_image_url(self, raw_new_dict: dict) -> Optional[str]:
        image_content = raw_new_dict.get("ns1:content")
        if image_content is None:
            return None
        return image_content.get("url")
