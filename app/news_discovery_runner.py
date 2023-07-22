from argparse import ArgumentParser
from typing import Dict

from bus_station.command_terminal.bus.synchronous.sync_command_bus import SyncCommandBus
from yandil.container import default_container

from application.discover_news.discover_news_command import DiscoverNewsCommand
from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    command_bus = default_container[SyncCommandBus]
    command = DiscoverNewsCommand(news_source=args["source"])
    command_bus.transport(command)


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="News discovery runner")
    arg_solver.add_argument("-s", "--source", required=True, help="News source")

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()
