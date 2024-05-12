import dataclasses
import logging

import internal.repositories.interfaces

from .. import interfaces


@dataclasses.dataclass(frozen=True)
class _EventWithPublisher:
    publisher: interfaces.PublisherId
    event: interfaces.Event


class PubSubBroker(interfaces.IPubSubBroker):
    def __init__(self):
        # usage: self.subscription[publisher][event_type] -> all callbacks
        self._subscriptions: dict[interfaces.PublisherId, dict[str, list[interfaces.Callback]]] = {}
        self._unprocessed_events: list[_EventWithPublisher] = []

    def publish(self, publisher: interfaces.PublisherId, event: interfaces.Event):
        logging.debug('publisher=%s has published event of type=%s', publisher, event.type)
        self._unprocessed_events.append(_EventWithPublisher(publisher, event))

    def subscribe(
        self,
        subscriber: interfaces.SubscriberId,
        publisher: interfaces.PublisherId,
        type: str,
        callback: interfaces.Callback,
    ):
        logging.debug(
            'subscriber=%s has subscribed to event of type=%s from publisher=%s',
            subscriber,
            type,
            publisher,
        )
        if publisher not in self._subscriptions:
            self._subscriptions[publisher] = {}
        if type not in self._subscriptions[publisher]:
            self._subscriptions[publisher][type] = []
        self._subscriptions[publisher][type].append(callback)

    def clear_events(self):
        events_cnt = len(self._unprocessed_events)
        self._unprocessed_events.clear()
        logging.debug('pub-sub events cleared, removed %d events', events_cnt)

    def process_published(self, repo: internal.repositories.interfaces.IRepository):
        logging.debug('processing published events')
        processed_cnt = 0
        while self._unprocessed_events:
            publisher, event = (
                self._unprocessed_events[0].publisher,
                self._unprocessed_events[0].event,
            )
            self._unprocessed_events = self._unprocessed_events[1:]
            if publisher not in self._subscriptions:
                continue
            if event.type not in self._subscriptions[publisher]:
                continue
            for callback in self._subscriptions[publisher][event.type]:
                callback(publisher, event, repo)
            processed_cnt += 1
        logging.debug('processed %d events', processed_cnt)
