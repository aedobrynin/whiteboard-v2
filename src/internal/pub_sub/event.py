import dataclasses


EventType = str


@dataclasses.dataclass
class Event:
    # TODO: publisher?
    type: EventType
