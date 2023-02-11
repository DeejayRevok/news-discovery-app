from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.confidencial"
            ".confidencial_response_to_news_transformer.ConfidencialResponseToNewsTransformer",
            "infrastructure.confidencial"
            ".confidencial_response_to_news_transformer.ConfidencialResponseToNewsTransformer",
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.confidencial.confidencial_news_fetcher.ConfidencialNewsFetcher",
            "infrastructure.confidencial.confidencial_news_fetcher.ConfidencialNewsFetcher",
            [
                Argument.no_kw_argument(
                    "@infrastructure.confidencial"
                    ".confidencial_response_to_news_transformer.ConfidencialResponseToNewsTransformer"
                )
            ],
        )
    )
