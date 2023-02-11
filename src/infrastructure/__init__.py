from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition

from infrastructure.abc import load as load_abc
from infrastructure.confidencial import load as load_confidencial
from infrastructure.politico import load as load_politico


def load() -> None:
    load_abc()
    load_politico()
    load_confidencial()

    container_builder.set_definition(
        Definition(
            "infrastructure.third_party_news_fetcher_selector.ThirdPartyNewsFetcherSelector",
            "infrastructure.third_party_news_fetcher_selector.ThirdPartyNewsFetcherSelector",
            [
                Argument.no_kw_argument("@infrastructure.abc.abc_news_fetcher.ABCNewsFetcher"),
                Argument.no_kw_argument(
                    "@infrastructure.confidencial.confidencial_news_fetcher.ConfidencialNewsFetcher"
                ),
                Argument.no_kw_argument("@infrastructure.politico.politico_news_fetcher.PoliticoNewsFetcher"),
            ],
        )
    )
