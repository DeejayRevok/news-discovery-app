from discovery.adapters.abc_rss_news_adapter import ABCRssNewsAdapter
from discovery.adapters.elconfidencial_rss_news_adapter import ConfidencialRssNewsAdapter
from discovery.fetch_implementations.fetch_rss_news_implementation import FetchRssNewsImplementation

DEFINITIONS = {
    "fetch_abc_rss_news": {
        "class": FetchRssNewsImplementation,
        "cron_expression": "*/10 * * * *",
        "source_adapters": [ABCRssNewsAdapter],
        "abc_rss": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
    },
    "fetch_confidencial_rss_news": {
        "class": FetchRssNewsImplementation,
        "cron_expression": "*/10 * * * *",
        "source_adapters": [ConfidencialRssNewsAdapter],
        "el_confidencial_rss": "https://rss.elconfidencial.com/mundo/",
    },
}
