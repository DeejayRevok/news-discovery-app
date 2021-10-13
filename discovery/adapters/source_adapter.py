from abc import abstractmethod
from typing import Iterator, Any

from news_service_lib.models.new import New

from log_config import get_logger

LOGGER = get_logger()


class SourceAdapter:
    def __init__(self, source_params: dict):
        self.source_params = source_params

    def fetch(self) -> Iterator[New]:
        return self.adapt(self._fetch())

    def adapt(self, fetched_items: Iterator[Any]) -> Iterator[New]:
        for item in fetched_items:
            try:
                yield self._adapt_single(item)
            except Exception as ex:
                LOGGER.error("Error while adapting new: %s", str(ex))

    @abstractmethod
    def _fetch(self) -> Iterator[Any]:
        pass

    @abstractmethod
    def _adapt_single(self, item: Any) -> New:
        pass
