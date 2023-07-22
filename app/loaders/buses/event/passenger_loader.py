from bus_station.event_terminal.event import Event
from bus_station.passengers.passenger_mapper import passenger_mapper

from domain.new.new_discovered_event import NewDiscoveredEvent


def load() -> None:
    passenger_mapper(NewDiscoveredEvent, Event, "event.new_discovered")
