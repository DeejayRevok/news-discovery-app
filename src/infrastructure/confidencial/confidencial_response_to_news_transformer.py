from time import mktime, strptime
from typing import Iterable, Optional
from xml.etree.ElementTree import fromstring, Element, tostring

from bs4 import BeautifulSoup
from lxml import html
from xmltodict import parse
from requests import Response

from domain.new.language import Language
from domain.new.new import New
from domain.new.news_source import NewsSource


class ConfidencialResponseToNewsTransformer:
    __DATE_INPUT_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    __ROOT_NEW_TAG = "{http://www.w3.org/2005/Atom}entry"

    def transform(self, response: Response) -> Iterable[New]:
        rss = fromstring(response.content)
        for element in rss:
            if element.tag != self.__ROOT_NEW_TAG:
                continue

            new = self.__transform_element_to_new(element)
            yield new

    def __transform_element_to_new(self, element: Element) -> New:
        raw_new_dict = parse(tostring(element).decode(), attr_prefix="")["ns0:entry"]
        content = self.__parse_content(raw_new_dict["ns0:content"]["#text"])
        url = next(filter(lambda link: link["rel"] == "alternate", raw_new_dict["ns0:link"]), dict(href=""))["href"]
        date = mktime(strptime(raw_new_dict["ns0:published"], self.__DATE_INPUT_FORMAT))

        return New(
            title=raw_new_dict["ns0:title"],
            url=url,
            content=content,
            source=NewsSource.CONFIDENCIAL,
            date=date,
            language=Language.SPANISH,
            image=self.__get_image_url(raw_new_dict),
        )

    def __parse_content(self, html_string: str) -> str:
        if html.fromstring(html_string).find(".//*") is not None:
            html_content = BeautifulSoup(html_string, "html.parser").text
            return self.__parse_content(html_content)
        else:
            return html_string

    def __get_image_url(self, raw_new_dict: dict) -> Optional[str]:
        image_content = raw_new_dict.get("ns2:content")
        if image_content is None:
            return None
        return image_content.get("url")
