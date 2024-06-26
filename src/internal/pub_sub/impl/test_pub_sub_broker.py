import pytest

import internal.repositories.interfaces
import internal.repositories.mocks

from .pub_sub_broker import PubSubBroker
from ..interfaces import Event, PublisherId


@pytest.fixture(name='callback_mock')
def _callback_mock():
    class Mock:
        calls: list[tuple[PublisherId, Event, internal.repositories.interfaces.IRepository]]

        def __init__(self):
            self.calls = []

        def __call__(
            self,
            publisher: PublisherId,
            event: Event,
            repo: internal.repositories.interfaces.IRepository,
        ):
            self.calls.append((publisher, event, repo))

    def wrapper():
        return Mock()

    return wrapper


def test_pub_sub_broker_processing(callback_mock):
    broker = PubSubBroker()

    repo_mock = internal.repositories.mocks.MockRepository()

    publisher_id = 'pub'
    subscriber_id = 'sub'

    event = Event(type='type')

    subscriber_callback = callback_mock()

    broker.subscribe(subscriber_id, publisher_id, event.type, subscriber_callback)
    broker.publish(publisher_id, event)
    assert len(subscriber_callback.calls) == 0
    broker.process_published(repo_mock)
    assert subscriber_callback.calls == [(publisher_id, event, repo_mock)]


def test_pub_sub_broker_event_from_different_publisher_does_not_trigger_callback():
    # TODO
    pass


def test_pub_sub_broker_event_of_different_type_does_not_trigger_callback():
    # TODO
    pass


def test_pub_sub_broker_processed_events_are_flushed(callback_mock):
    broker = PubSubBroker()

    repo_mock = internal.repositories.mocks.MockRepository()

    publisher_id = 'pub'
    subscriber_id = 'sub'

    event = Event(type='type')

    subscriber_callback = callback_mock()

    broker.subscribe(subscriber_id, publisher_id, event.type, subscriber_callback)
    broker.publish(publisher_id, event)
    assert len(subscriber_callback.calls) == 0
    broker.process_published(repo_mock)
    assert subscriber_callback.calls == [(publisher_id, event, repo_mock)]
    subscriber_callback.calls = []
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 0


def test_pub_sub_broker_clearing_events(callback_mock):
    broker = PubSubBroker()

    repo_mock = internal.repositories.mocks.MockRepository()

    publisher_id = 'pub'
    subscriber_id = 'sub'

    event = Event(type='type')

    subscriber_callback = callback_mock()

    broker.subscribe(subscriber_id, publisher_id, event.type, subscriber_callback)
    broker.publish(publisher_id, event)
    assert len(subscriber_callback.calls) == 0
    broker.clear_events()
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 0


def test_pub_sub_unsubscribe(callback_mock):
    publisher_id = 'pub'
    subscriber_id = 'sub'

    broker = PubSubBroker()
    repo_mock = internal.repositories.mocks.MockRepository()
    event = Event(type='type')
    subscriber_callback = callback_mock()
    broker.subscribe(subscriber_id, publisher_id, event.type, subscriber_callback)
    broker.publish(publisher_id, event)
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 1

    broker.unsubscribe(subscriber_id, publisher_id)
    broker.publish(publisher_id, event)
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 1


def test_pub_sub_unsubscribe_from_all(callback_mock):
    publisher_a_id = 'pub_a'
    publisher_b_id = 'pub_b'
    subscriber_id = 'sub'

    broker = PubSubBroker()
    repo_mock = internal.repositories.mocks.MockRepository()
    event = Event(type='type')
    subscriber_callback = callback_mock()
    broker.subscribe(subscriber_id, publisher_a_id, event.type, subscriber_callback)
    broker.subscribe(subscriber_id, publisher_b_id, event.type, subscriber_callback)

    broker.publish(publisher_a_id, event)
    broker.publish(publisher_b_id, event)
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 2

    broker.unsubscribe_from_all(
        subscriber_id,
    )
    broker.publish(publisher_a_id, event)
    broker.publish(publisher_b_id, event)
    broker.process_published(repo_mock)
    assert len(subscriber_callback.calls) == 2
