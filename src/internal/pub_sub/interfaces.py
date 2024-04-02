from __future__ import annotations
import abc
import dataclasses
from typing import Callable

import internal.repositories.interfaces


@dataclasses.dataclass
class Event:
    # TODO: type as objtype
    type: str


PubSubId = str
SubscriberId = PubSubId
PublisherId = PubSubId

Callback = Callable[[PublisherId, Event, internal.repositories.interfaces.IRepository], None]


class IPubSubBroker(abc.ABC):
    @abc.abstractmethod
    def publish(self, publisher: str, event: Event):
        pass

    @abc.abstractmethod
    def subscribe(
        self, subscriber: SubscriberId, publisher: PublisherId, type: str, callback: Callback
    ):
        pass

    # TODO: this probably should be in another class
    # (because now it is accessible from any object)
    @abc.abstractmethod
    def process_published(self, repo: internal.repositories.interfaces.IRepository):
        pass

    # TODO: unsubscribe method (will be useful in View)

    # TODO: unsubsribe_from_all method?
    # TODO: myb allow to subscribe on events of particular type published by anyone?
