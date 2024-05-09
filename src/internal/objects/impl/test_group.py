import internal.pub_sub.mocks
from internal.models import Position

from .group import BoardObjectGroup
from ..types import BoardObjectType
from .object_id import generate_object_id


def test_board_group_serialization():
    id = generate_object_id()
    type = BoardObjectType.GROUP
    children_ids = (generate_object_id(), generate_object_id())
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectGroup(id, broker, children_ids)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'children_ids': children_ids
    }


def test_board_group_deserialization():
    id = generate_object_id()
    type = BoardObjectType.GROUP
    children_ids = (generate_object_id(), generate_object_id())
    serialized = {
        'id': id,
        'type': type.value,
        'children_ids': children_ids
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectGroup = BoardObjectGroup.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.children_ids == children_ids
