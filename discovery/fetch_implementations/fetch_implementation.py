from abc import abstractmethod
from typing import Iterator

from news_service_lib.models.new import New


class FetchImplementation:
    def __init__(self, definition: dict):
        self.definition = definition

    @abstractmethod
    def __call__(self) -> Iterator[New]:
        pass
