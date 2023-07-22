from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from yandil.container import default_container

from application.discover_news.discover_news_command_handler import DiscoverNewsCommandHandler


def register() -> None:
    registry = default_container[CommandHandlerRegistry]
    registry.register(default_container[DiscoverNewsCommandHandler])
