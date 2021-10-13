from typing import Iterator

from news_service_lib.models.new import New

from discovery.fetch_implementations.fetch_implementation import FetchImplementation
from log_config import get_logger

LOGGER = get_logger()


class FetchRssNewsImplementation(FetchImplementation):
    def __init__(self, definition: dict):
        FetchImplementation.__init__(self, definition)

    def __call__(self) -> Iterator[New]:
        for adapter_class in self.definition["source_adapters"]:
            adapter = adapter_class(self.definition)
            yield from adapter.fetch()
