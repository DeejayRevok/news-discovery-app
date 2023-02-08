from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.abc.abc_response_to_news_transformer.ABCResponseToNewsTransformer",
            "infrastructure.abc.abc_response_to_news_transformer.ABCResponseToNewsTransformer",
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.abc.abc_news_fetcher.ABCNewsFetcher",
            "infrastructure.abc.abc_news_fetcher.ABCNewsFetcher",
            [
                Argument.no_kw_argument(
                    "@infrastructure.abc.abc_response_to_news_transformer.ABCResponseToNewsTransformer"
                )
            ],
        )
    )
