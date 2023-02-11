from time import mktime, strptime
from typing import Iterable

from xml.etree.ElementTree import fromstring, Element, tostring
from bs4 import BeautifulSoup
from lxml import html
from xmltodict import parse
from requests import Response

from domain.new.language import Language
from domain.new.new import New
from domain.new.news_source import NewsSource


class ABCResponseToNewsTransformer:
    __DATE_INPUT_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
    __ROOT_NEW_TAG = "item"

    def transform(self, response: Response) -> Iterable[New]:
        rss = fromstring(response.content)
        for channel in rss:
            for element in channel:
                if element.tag != self.__ROOT_NEW_TAG:
                    continue

                yield self.__transform_element_to_new(element)

    def __transform_element_to_new(self, element: Element) -> New:
        new_dict = parse(tostring(element).decode(), attr_prefix="")[self.__ROOT_NEW_TAG]
        content = self.__parse_content(new_dict["description"])
        date = mktime(strptime(new_dict["pubDate"], self.__DATE_INPUT_FORMAT))

        return New(
            title=new_dict["title"],
            url=new_dict["link"],
            content=content,
            source=NewsSource.ABC,
            date=date,
            language=Language.SPANISH,
        )

    def __parse_content(self, html_string: str) -> str:
        if html.fromstring(html_string).find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self.__parse_content(html_content)
        else:
            return html_string
