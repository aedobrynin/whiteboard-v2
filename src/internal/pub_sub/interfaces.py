from __future__ import annotations
import abc
from typing import Callable

import internal.repositories.interfaces
from .event import Event, EventType

PubSubId = str
SubscriberId = PubSubId
PublisherId = PubSubId

Callback = Callable[[PublisherId, Event, internal.repositories.interfaces.IRepository], None]


class IPubSubBroker(abc.ABC):
    @abc.abstractmethod
    def publish(self, publisher: PublisherId, event: Event):
        pass

    @abc.abstractmethod
    def subscribe(
        self, subscriber: SubscriberId, publisher: PublisherId, type: EventType, callback: Callback
    ):
        pass

    @abc.abstractmethod
    def clear_events(self):
        pass

    # TODO: this probably should be in another class
    # (because now it is accessible from any object)
    @abc.abstractmethod
    def process_published(self, repo: internal.repositories.interfaces.IRepository):
        pass

    @abc.abstractmethod
    def unsubscribe(self, subscriber: SubscriberId, publisher: PublisherId):
        """Unsubscribe from all events of publisher"""
        pass

    @abc.abstractmethod
    def unsubscribe_from_all(self, subscriber: SubscriberId):
        """Unsubscribe from all events"""
        pass

    # TODO: myb allow to subscribe on events of particular type published by anyone?
