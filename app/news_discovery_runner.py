from argparse import ArgumentParser
from typing import Dict

from bus_station.command_terminal.bus.command_bus import CommandBus
from pypendency.builder import container_builder

from application.discover_news.discover_news_command import DiscoverNewsCommand
from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    command_bus: CommandBus = container_builder.get("bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus")
    command = DiscoverNewsCommand(news_source=args["source"])
    command_bus.transport(command)


def __load_args() -> Dict:
    arg_solver = ArgumentParser(description="News discovery runner")
    arg_solver.add_argument("-s", "--source", required=True, help="News source")

    return vars(arg_solver.parse_args())


if __name__ == "__main__":
    run()