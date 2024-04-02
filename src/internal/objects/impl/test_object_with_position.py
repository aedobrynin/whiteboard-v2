import uuid

import internal.pub_sub.mocks
from internal.models import Position

from .object_with_position import BoardObjectWithPosition
from ..types import BoardObjectType


def test_board_object_with_position_serialization():
    _id = uuid.uuid4()
    _type = BoardObjectType.CARD
    position = Position(1, 2, 3)

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition(_id, _type, position, broker)
    assert obj.serialize() == {
        'id': str(_id),
        'type': _type.value,
        'position': position.serialize(),
    }


def test_board_object_with_position_deserialization():
    _id = uuid.uuid4()
    _type = BoardObjectType.CARD
    position = Position(1, 2, 3)

    serialized = {
        'id': str(_id),
        'type': _type.value,
        'position': position.serialize(),
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition.from_serialized(serialized, broker)
    assert obj.id == _id
    assert obj.type == _type
    assert obj.position == position
