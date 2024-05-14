import dataclasses
import logging
import collections

import internal.repositories.interfaces

from .. import interfaces


@dataclasses.dataclass(frozen=True)
class _EventWithPublisher:
    publisher: interfaces.PublisherId
    event: interfaces.Event


class PubSubBroker(interfaces.IPubSubBroker):
    def __init__(self):
        # usage: self._entity_subscribers[publisher_id][event_type][subscriber_id] -> callback
        self._entity_subscribers: collections.defaultdict[
            interfaces.PublisherId,
            collections.defaultdict[
                interfaces.EventType, dict[interfaces.SubscriberId, interfaces.Callback]
            ],
        ] = collections.defaultdict(lambda: collections.defaultdict(dict))

        # usage: self._entity_subscriptions[subscriber_id][publisher_id] -> [type_a, type_b, ...]
        self._entity_subscriptions: collections.defaultdict[
            interfaces.SubscriberId,
            collections.defaultdict[interfaces.PublisherId, list[interfaces.EventType]],
        ] = collections.defaultdict(lambda: collections.defaultdict(list))

        self._unprocessed_events: list[_EventWithPublisher] = []

    def publish(self, publisher: interfaces.PublisherId, event: interfaces.Event):
        logging.debug('publisher=%s has published event of type=%s', publisher, event.type)
        self._unprocessed_events.append(_EventWithPublisher(publisher, event))

    def subscribe(
        self,
        subscriber: interfaces.SubscriberId,
        publisher: interfaces.PublisherId,
        type: interfaces.EventType,
        callback: interfaces.Callback,
    ):
        logging.debug(
            'subscriber=%s has subscribed to event of type=%s from publisher=%s',
            subscriber,
            type,
            publisher,
        )
        if subscriber in self._entity_subscribers[publisher][type]:
            logging.warning(
                'subscriber=%s is already subscribed to event of type=%s from publisher=%s',
                subscriber,
                type,
                publisher,
            )
        self._entity_subscribers[publisher][type][subscriber] = callback
        self._entity_subscriptions[subscriber][publisher].append(type)

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
            if publisher not in self._entity_subscribers:
                continue
            if event.type not in self._entity_subscribers[publisher]:
                continue
            for callback in self._entity_subscribers[publisher][event.type].values():
                callback(publisher, event, repo)
            processed_cnt += 1
        logging.debug('processed %d events', processed_cnt)

    def unsubscribe(self, subscriber: interfaces.SubscriberId, publisher: interfaces.PublisherId):
        # TODO: myb raise exception if no info about subscriber?
        for type in self._entity_subscriptions[subscriber][publisher]:
            del self._entity_subscribers[publisher][type][subscriber]
        del self._entity_subscriptions[subscriber][publisher]

    def unsubscribe_from_all(self, subscriber: interfaces.SubscriberId):
        # TODO: myb raise exception if no info about subscriber?
        for publisher, types in self._entity_subscriptions[subscriber].items():
            for type in types:
                del self._entity_subscribers[publisher][type][subscriber]
        del self._entity_subscriptions[subscriber]
