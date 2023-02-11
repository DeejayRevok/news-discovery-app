from abc import abstractmethod
from typing import Protocol, Iterable

from domain.new.new import New


class NewsFetcher(Protocol):
    @abstractmethod
    def fetch(self) -> Iterable[New]:
        pass
