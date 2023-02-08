from dataclasses import dataclass

from bus_station.command_terminal.command import Command


@dataclass(frozen=True)
class DiscoverNewsCommand(Command):
    news_source: str

    @classmethod
    def passenger_name(cls) -> str:
        return "command.news_discovery.discover_news"
