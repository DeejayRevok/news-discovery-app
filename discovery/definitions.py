from discovery.adapters.abc_rss_news_adapter import ABCRssNewsAdapter
from discovery.adapters.cbs_san_francisco_rss_news_adapter import CBSSanFranciscoRSSNewsAdapter
from discovery.adapters.elconfidencial_rss_news_adapter import ConfidencialRssNewsAdapter
from discovery.adapters.politco_rss_news_adapter import PoliticoRSSNewsAdapter
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
    "fetch_cbs_san_francisco_rss_news": {
        "class": FetchRssNewsImplementation,
        "cron_expression": "*/10 * * * *",
        "source_adapters": [CBSSanFranciscoRSSNewsAdapter],
        "cbs_sf_rss": "https://sanfrancisco.cbslocal.com/feed/",
    },
    "fetch_politico_rss_news": {
        "class": FetchRssNewsImplementation,
        "cron_expression": "*/10 * * * *",
        "source_adapters": [PoliticoRSSNewsAdapter],
        "politico_rss": "https://www.politico.com/rss/politicopicks.xml",
    },
}
