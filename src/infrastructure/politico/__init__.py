from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.politico.politico_response_to_news_transformer.PoliticoResponseToNewsTransformer",
            "infrastructure.politico.politico_response_to_news_transformer.PoliticoResponseToNewsTransformer",
        )
    )
    container_builder.set_definition(
        Definition(
            "infrastructure.politico.politico_news_fetcher.PoliticoNewsFetcher",
            "infrastructure.politico.politico_news_fetcher.PoliticoNewsFetcher",
            [
                Argument.no_kw_argument(
                    "@infrastructure.politico.politico_response_to_news_transformer.PoliticoResponseToNewsTransformer"
                )
            ],
        )
    )
