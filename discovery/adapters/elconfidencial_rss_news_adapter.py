from news_service_lib.models.language import Language
from time import mktime, strptime
from typing import Iterator
from xml.etree.ElementTree import Element, fromstring, tostring

import requests
from bs4 import BeautifulSoup
from lxml import html
from news_service_lib.models.new import New
from xmltodict import parse

from discovery.adapters.source_adapter import SourceAdapter
from log_config import get_logger

LOGGER = get_logger()


class ConfidencialRssNewsAdapter(SourceAdapter):
    DATE_INPUT_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
    ROOT_NEW_TAG = "{http://www.w3.org/2005/Atom}entry"

    def _fetch(self) -> Iterator[Element]:
        LOGGER.info("Fetching news from %s", self.source_params["el_confidencial_rss"])
        response = requests.get(self.source_params["el_confidencial_rss"])
        rss = fromstring(response.content)
        for item in rss:
            if item.tag == self.ROOT_NEW_TAG:
                yield item

    def _adapt_single(self, item: Element) -> New:
        new_dict = parse(tostring(item).decode(), attr_prefix="")["ns0:entry"]
        LOGGER.info("Found new with title %s", new_dict["ns0:title"])

        content = self._parse_content(new_dict["ns0:content"]["#text"])
        url = next(filter(lambda link: link["rel"] == "alternate", new_dict["ns0:link"]), dict(href=""))["href"]

        date = mktime(strptime(new_dict["ns0:published"], "%Y-%m-%dT%H:%M:%S%z"))

        return New(
            title=new_dict["ns0:title"],
            url=url,
            content=content,
            source="El Confidencial",
            date=date,
            language=Language.SPANISH,
        )

    def _parse_content(self, html_string: str) -> str:
        if html.fromstring(html_string).find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self._parse_content(html_content)
        else:
            return html_string
