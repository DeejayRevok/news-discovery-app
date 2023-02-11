from domain.new.news_source import NewsSource


class NewsFetcherNotImplementedException(Exception):
    def __init__(self, news_source: NewsSource):
        self.news_source = news_source
        super().__init__(f"News fetcher for source {news_source.value} not implemented")
