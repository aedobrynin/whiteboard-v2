import dataclasses

import internal.repositories.interfaces

from .. import interfaces


@dataclasses.dataclass(frozen=True)
class PublishedEvent:
    publisher: interfaces.PublisherId
    event: interfaces.Event


class MockPubSubBroker(interfaces.IPubSubBroker):
    def __init__(self):
        self._published = []

    @property
    def published(self) -> list[PublishedEvent]:
        return self._published

    def publish(self, publisher: interfaces.PublisherId, event: interfaces.Event):
        self._published.append(PublishedEvent(publisher, event))

    def subscribe(
        self,
        subscriber: interfaces.SubscriberId,
        publisher: interfaces.PublisherId,
        type: str,
        callback: interfaces.Callback,
    ):
        # TODO: implement when needed
        pass

    def process_published(self, repo: internal.repositories.interfaces.IRepository):
        # TODO: implement when needed
        pass
