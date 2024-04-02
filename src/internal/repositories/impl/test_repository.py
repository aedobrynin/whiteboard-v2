import pytest
import uuid

from . import repository
from .. import exceptions
import internal.objects
import internal.pub_sub.mocks


@pytest.fixture(name='get_serialized_card')
def _get_serialized_card():
    def _impl():
        return {
            'id': '4680838b-4217-4992-9932-3d3ebb22c8ec',
            'position': {
                'x': 1,
                'y': 2,
                'z': 3,
            },
            'text': 'text',
            'type': 'card',
        }

    return _impl


def test_repository_add_object(get_serialized_card):
    repo = repository.Repository([])
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get_updated() == {
        obj.id: get_serialized_card(),
    }


def test_repository_get_object(get_serialized_card):
    repo = repository.Repository([])
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get(obj.id) == obj


def test_repository_get_object_from_init(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj])
    assert repo.get(obj.id) == obj


def test_repository_add_with_same_id(get_serialized_card):
    repo = repository.Repository([])
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    with pytest.raises(exceptions.ObjectAlreadyExistsException):
        repo.add(obj)
    assert repo.get(obj.id) == obj


def test_repository_update_object(get_serialized_card):
    repo = repository.Repository([])
    broker = internal.pub_sub.mocks.MockPubSubBroker()

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
    repo = repository.Repository([])
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo.add(obj)
    assert repo.get_updated() == {
        obj.id: get_serialized_card(),
    }
    assert len(repo.get_updated()) == 0


def test_repository_delete_object(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj])

    repo.delete(obj.id)
    assert repo.get(obj.id) is None
    assert repo.get_updated() == {
        obj.id: None,
    }


def test_repository_delete_raises_on_unknown_id():
    repo = repository.Repository([])
    with pytest.raises(exceptions.ObjectNotFound):
        repo.delete(uuid.uuid4())


def test_repository_delete_object_updates_are_flushed(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj])

    repo.delete(obj.id)
    assert repo.get_updated() == {
        obj.id: None,
    }
    assert len(repo.get_updated()) == 0


def test_repository_no_updates_after_init(get_serialized_card):
    broker = internal.pub_sub.mocks.MockPubSubBroker()
    obj = internal.objects.build_from_serialized(get_serialized_card(), broker)
    repo = repository.Repository([obj])
    assert len(repo.get_updated()) == 0


# TODO: test pub_sub events
