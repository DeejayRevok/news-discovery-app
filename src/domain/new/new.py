from dataclasses import dataclass
from typing import Optional

from domain.new.language import Language
from domain.new.news_source import NewsSource


@dataclass
class New:
    title: str
    url: str
    content: str
    source: NewsSource
    date: float
    language: Language
    image: Optional[str] = None
