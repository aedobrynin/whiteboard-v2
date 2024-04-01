from .. import interfaces

import internal.repositories.interfaces


class MockPubSubBroker(interfaces.IPubSubBroker):
    def __init__(self):
        pass

    def publish(self, publisher: interfaces.PublisherId, event: interfaces.Event):
        # TODO: implement when needed
        pass

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
