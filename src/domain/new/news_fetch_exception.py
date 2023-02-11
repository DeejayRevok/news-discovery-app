from domain.new.news_source import NewsSource


class NewsFetchException(Exception):
    def __init__(self, source: NewsSource, reason: str):
        self.source = source
        self.reason = reason
        super().__init__(f"Error fetching news from {source.value}. Reason: {reason}")
