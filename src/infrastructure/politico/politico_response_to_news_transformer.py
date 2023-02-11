from time import mktime, strptime
from typing import Iterable, Optional
from xml.etree.ElementTree import fromstring, Element, tostring

from bs4 import BeautifulSoup
from lxml import html
from lxml.etree import ParserError
from xmltodict import parse
from requests import Response

from domain.new.language import Language
from domain.new.new import New
from domain.new.news_source import NewsSource


class PoliticoResponseToNewsTransformer:
    __DATE_FORMAT = "%a, %d %b %Y %H:%M:%S EST"
    __ROOT_NEW_TAG = "item"

    def transform(self, response: Response) -> Iterable[New]:
        rss = fromstring(response.content)
        for channel in rss:
            for element in channel:
                if element.tag != self.__ROOT_NEW_TAG:
                    continue

                new = self.__transform_element_to_new(element)
                if new is None:
                    continue

                yield new

    def __transform_element_to_new(self, element: Element) -> Optional[New]:
        raw_new_dict = parse(tostring(element).decode(), attr_prefix="")[self.__ROOT_NEW_TAG]

        if "ns3:encoded" not in raw_new_dict:
            return None

        content = self.__parse_content(raw_new_dict["ns3:encoded"])
        if content is None:
            return None

        date = mktime(strptime(raw_new_dict["pubDate"], self.__DATE_FORMAT))

        return New(
            title=raw_new_dict["title"],
            url=raw_new_dict["link"],
            content=content,
            source=NewsSource.POLITICO,
            date=date,
            language=Language.ENGLISH,
            image=self.__get_image_url(raw_new_dict),
        )

    def __parse_content(self, html_string: str) -> Optional[str]:
        try:
            html_document = html.fromstring(html_string)
        except ParserError as perr:
            if str(perr) == "Document is empty":
                return None
            raise perr

        if html_document.find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self.__parse_content(html_content)
        else:
            return html_string

    def __get_image_url(self, raw_new_dict: dict) -> Optional[str]:
        image_content = raw_new_dict.get("ns1:content")
        if image_content is None:
            return None
        return image_content.get("url")
