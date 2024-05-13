from datetime import datetime

import pytest

import internal.objects.interfaces
import internal.pub_sub.mocks
from . import repository
from .. import events
from .. import exceptions
from .. import interfaces


@pytest.fixture(name='get_serialized_card')
def _get_serialized_card():
    def _impl():
        return {
            'id': '4680838b-4217-4992-9932-3d3ebb22c8ec',
            'create_dttm': datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ'),
            'position': {
                'x': 1,
                'y': 2,
                'z': 3,
            },
            'text': 'text',
            'type': 'card',
            'font': {
                'slant': 'roman',
                'weight': 'normal',
                'color': 'black',
                'family': 'Arial',
                'size': 14,
            },
            'color': 'light yellow',
            'width': 100,
            'height': 150,
        }

    return _impl


def test_repository_add_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get_updated() == {
        obj.id: get_serialized_card(),
    }
<<<<<<< HEAD
    assert len(broker.published) == 6  # other notifications come
=======
    assert len(broker.published) == 9  # other notifications come
>>>>>>> main
    event = broker.published[-1]  # the last notification is added object
    assert event == internal.pub_sub.mocks.PublishedEvent(
        interfaces.REPOSITORY_PUB_SUB_ID,
        events.EventObjectAdded(obj.id),
    )


def test_repository_get_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get(obj.id) == obj


def test_repository_get_all_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    data = get_serialized_card()
    obj1 = internal.objects.build_from_serialized(data, broker)
    repo.add(obj1)
    data['id'] = 'another_id'
    obj2 = internal.objects.build_from_serialized(data, broker)
    repo.add(obj2)
    assert {repo.get_all() == [obj1, obj2]}


def test_repository_get_object_from_init(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj], broker)
    assert repo.get(obj.id) == obj


def test_repository_add_with_same_id(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert len(broker.published) == 9  # some other notifications come
    with pytest.raises(exceptions.ObjectAlreadyExistsException):
        repo.add(obj)
    assert repo.get(obj.id) == obj
    assert len(broker.published) == 9  # some other notifications come


def test_repository_update_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    obj: internal.objects.interfaces.IBoardObjectCard = internal.objects.build_from_serialized(
        get_serialized_card(), broker
    )  # type: ignore
    repo.add(obj)
    assert repo.get_updated() == {
        obj.id: get_serialized_card(),
    }

    obj.text = 'updated_text'
    assert repo.get_updated() == {
        obj.id: obj.serialize(),
    }


def test_repository_updates_flush(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get_updated() == {
        obj.id: get_serialized_card(),
    }
    assert len(repo.get_updated()) == 0


def test_repository_delete_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj], broker)

    repo.delete(obj.id)
    assert repo.get(obj.id) is None
    assert repo.get_updated() == {
        obj.id: None,
    }
    assert len(broker.published) == 9  # some other notifications came
    event = broker.published[-1]  # the last notification is added object
    assert event == internal.pub_sub.mocks.PublishedEvent(
        interfaces.REPOSITORY_PUB_SUB_ID, events.EventObjectDeleted(obj.id)
    )


def test_repository_delete_raises_on_unknown_id():
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    repo = repository.Repository([], broker)
    with pytest.raises(exceptions.ObjectNotFound):
        repo.delete('123')
    assert len(broker.published) == 0


def test_repository_delete_object_updates_are_flushed(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj], broker)

    repo.delete(obj.id)
    assert repo.get_updated() == {
        obj.id: None,
    }
    assert len(repo.get_updated()) == 0


def test_repository_no_updates_after_init(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj], broker)
    assert len(repo.get_updated()) == 0
    # some notifications came
    assert len(broker.published) == 8  # TODO: myb it will be changed in future
