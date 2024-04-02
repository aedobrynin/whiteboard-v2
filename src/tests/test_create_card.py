import pytest
import dataclasses

import internal.pub_sub.interfaces
import internal.pub_sub.impl
import internal.repositories.interfaces
import internal.repositories.impl
import internal.objects
import internal.objects.interfaces
import internal.models
import internal.repositories.events
import internal.storages.impl
import internal.controller.impl


# TODO: better (and move it somewhere)
@dataclasses.dataclass(frozen=True)
class _PubSubEvent:
    publisher_id: internal.pub_sub.interfaces.PublisherId
    event: internal.pub_sub.interfaces.Event


@pytest.fixture(name='get_mock_pub_sub_callback')
def _get_mock_pub_sub_callback():
    class _Impl:
        def __init__(self):
            self._calls = []

        @property
        def calls(self) -> list[_PubSubEvent]:
            return self._calls

        def __call__(
            self,
            publisher_id: internal.pub_sub.interfaces.PublisherId,
            event: internal.pub_sub.Event,
            repo: internal.repositories.interfaces.IRepository,
        ):
            self._calls.append(_PubSubEvent(publisher_id, event))

    def _impl():
        return _Impl()

    return _impl


def test_create_object(tmp_path, get_mock_pub_sub_callback):
    type_ = internal.objects.BoardObjectType.CARD
    position = internal.models.Position(1, 2, 3)

    # TODO: is this bad that we access 'impl' directly?
    storage = internal.storages.impl.LocalYDocStorage(tmp_path / 'storage')
    broker = internal.pub_sub.impl.PubSubBroker()
    repo = internal.repositories.impl.Repository([], broker)

    add_object_callback = get_mock_pub_sub_callback()
    broker.subscribe(
        'mock',
        internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
        internal.repositories.events.EVENT_TYPE_OBJECT_ADDED,
        add_object_callback,
    )

    controller = internal.controller.impl.Controller(repo, storage, broker)
    controller.create_object(
        type_,
        position,
    )

    assert len(repo.get_updated()) == 0
    serialized_objects = storage.get_serialized_objects()
    assert len(serialized_objects) == 1

    serialized_obj = list(serialized_objects.values())[0]
    obj: internal.objects.interfaces.IBoardObjectCard = internal.objects.build_from_serialized(
        serialized_obj, broker
    )   # type: ignore
    assert isinstance(obj, internal.objects.interfaces.IBoardObjectCard)
    assert obj.type == type_
    assert obj.position == position
    # TODO: default text as const
    assert obj.text == 'text'

    assert add_object_callback.calls == [
        _PubSubEvent(
            internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EventObjectAdded(obj.id),
        )
    ]
